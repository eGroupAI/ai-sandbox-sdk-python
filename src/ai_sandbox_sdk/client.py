from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any, Dict, Generator, Optional

import requests

from .http_policy import should_retry_transient_http


class ApiError(RuntimeError):
  def __init__(self, status: int, body: str, trace_id: Optional[str] = None) -> None:
    super().__init__(f"HTTP {status}: {body}")
    self.status = status
    self.body = body
    self.trace_id = trace_id


@dataclass
class AiSandboxClient:
  base_url: str
  api_key: str
  timeout_seconds: int = 30
  max_retries: int = 2

  def __post_init__(self) -> None:
    self.base_url = self.base_url.rstrip("/")
    self._session = requests.Session()
    self._session.headers.update({
      "Authorization": f"Bearer {self.api_key}",
    })

  def _request(self, method: str, path: str, json_body: Optional[Dict[str, Any]] = None, accept: str = "application/json") -> requests.Response:
    attempt = 0
    while True:
      try:
        response = self._session.request(
          method=method,
          url=f"{self.base_url}/api/v1{path}",
          json=json_body,
          headers={"Accept": accept},
          timeout=self.timeout_seconds,
          stream=accept == "text/event-stream",
        )
      except requests.RequestException as exc:
        if attempt < self.max_retries:
          attempt += 1
          time.sleep(0.2 * attempt)
          continue
        raise RuntimeError(f"Network error: {exc}") from exc

      if should_retry_transient_http(method, response.status_code) and attempt < self.max_retries:
        attempt += 1
        time.sleep(0.2 * attempt)
        continue
      if response.status_code >= 400:
        raise ApiError(response.status_code, response.text, response.headers.get("x-trace-id"))
      return response

  def _json(self, method: str, path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
    return self._request(method, path, json_body=json_body).json()

  def create_agent(self, payload: Dict[str, Any]) -> Any: return self._json("POST", "/agents", payload)
  def update_agent(self, agent_id: int, payload: Dict[str, Any]) -> Any: return self._json("PUT", f"/agents/{agent_id}", payload)
  def list_agents(self, query: str = "") -> Any: return self._json("GET", f"/agents{f'?{query}' if query else ''}")
  def get_agent_detail(self, agent_id: int) -> Any: return self._json("GET", f"/agents/{agent_id}")
  def create_chat_channel(self, agent_id: int, payload: Dict[str, Any]) -> Any: return self._json("POST", f"/agents/{agent_id}/channels", payload)
  def send_chat(self, agent_id: int, payload: Dict[str, Any]) -> Any: return self._json("POST", f"/agents/{agent_id}/chat", payload)
  def get_chat_history(self, agent_id: int, channel_id: str, query: str = "limit=50&page=0") -> Any: return self._json("GET", f"/agents/{agent_id}/channels/{channel_id}/messages?{query}")
  def get_knowledge_base_articles(self, agent_id: int, collection_id: int, query: str = "startIndex=0") -> Any: return self._json("GET", f"/agents/{agent_id}/collections/{collection_id}/articles?{query}")
  def create_knowledge_base(self, agent_id: int, payload: Dict[str, Any]) -> Any: return self._json("POST", f"/agents/{agent_id}/collections", payload)
  def update_knowledge_base_status(self, agent_collection_id: int, payload: Dict[str, Any]) -> Any: return self._json("PATCH", f"/agent-collections/{agent_collection_id}/status", payload)
  def list_knowledge_bases(self, agent_id: int, query: str = "activeOnly=false") -> Any: return self._json("GET", f"/agents/{agent_id}/collections?{query}")

  def send_chat_stream(self, agent_id: int, payload: Dict[str, Any]) -> Generator[str, None, None]:
    response = self._request("POST", f"/agents/{agent_id}/chat", json_body=payload, accept="text/event-stream")
    for line in response.iter_lines(decode_unicode=True):
      if not line or not line.startswith("data: "):
        continue
      data = line[6:].strip()
      if data == "[DONE]":
        break
      yield data
