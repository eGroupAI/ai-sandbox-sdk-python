import unittest

from ai_sandbox_sdk.http_policy import should_retry_transient_http


class TestHttpPolicy(unittest.TestCase):
  def test_transient_retry_idempotent_only(self) -> None:
    self.assertTrue(should_retry_transient_http("GET", 503))
    self.assertFalse(should_retry_transient_http("POST", 503))
    self.assertFalse(should_retry_transient_http("GET", 404))


if __name__ == "__main__":
  unittest.main()
