from __future__ import annotations

import unittest
from unittest.mock import Mock

import requests

from ai_sandbox_sdk.client import AiSandboxClient, ApiError


class FakeResponse:
  def __init__(
      self,
      status_code: int,
      text: str = "",
      json_payload: dict | None = None,
      headers: dict[str, str] | None = None,
      lines: list[str] | None = None,
  ) -> None:
    self.status_code = status_code
    self.text = text
    self._json_payload = json_payload or {}
    self.headers = headers or {}
    self._lines = lines or []
    self.closed = False

  def json(self) -> dict:
    return self._json_payload

  def iter_lines(self, decode_unicode: bool = True):
    del decode_unicode
    for line in self._lines:
      yield line

  def close(self) -> None:
    self.closed = True


class TestClientContract(unittest.TestCase):
  def setUp(self) -> None:
    self.client = AiSandboxClient(
      base_url="https://api.example.test",
      api_key="test-key",
      timeout_seconds=1,
      max_retries=2,
    )

  def test_get_retries_on_transient_5xx(self) -> None:
    first = FakeResponse(503, text="temporary failure")
    second = FakeResponse(200, json_payload={"ok": True, "payload": {"items": []}})
    self.client._session.request = Mock(side_effect=[first, second])

    result = self.client.list_agents()

    self.assertEqual(2, self.client._session.request.call_count)
    self.assertTrue(first.closed)
    self.assertEqual({"ok": True, "payload": {"items": []}}, result)

  def test_post_does_not_retry_on_http_5xx(self) -> None:
    failed = FakeResponse(503, text="write failed", headers={"x-trace-id": "trace-post-1"})
    self.client._session.request = Mock(return_value=failed)

    with self.assertRaises(ApiError) as context:
      self.client.send_chat(123, {"channelId": "c-1", "message": "hello"})

    self.assertEqual(1, self.client._session.request.call_count)
    self.assertEqual(503, context.exception.status)
    self.assertEqual("trace-post-1", context.exception.trace_id)

  def test_post_retries_on_network_failure(self) -> None:
    success = FakeResponse(200, json_payload={"ok": True, "payload": {"messageId": "m-1"}})
    self.client._session.request = Mock(side_effect=[requests.Timeout("timeout"), success])

    result = self.client.send_chat(123, {"channelId": "c-1", "message": "hello"})

    self.assertEqual(2, self.client._session.request.call_count)
    self.assertEqual({"ok": True, "payload": {"messageId": "m-1"}}, result)

  def test_stream_closes_response_after_done(self) -> None:
    stream_response = FakeResponse(
      200,
      lines=["data: chunk-1", "data: [DONE]", "data: chunk-2"],
    )
    self.client._session.request = Mock(return_value=stream_response)

    chunks = list(self.client.send_chat_stream(123, {"channelId": "c-1", "message": "hello", "stream": True}))

    self.assertEqual(["chunk-1"], chunks)
    self.assertTrue(stream_response.closed)


if __name__ == "__main__":
  unittest.main()
