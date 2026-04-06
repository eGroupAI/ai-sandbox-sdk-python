import unittest

from ai_sandbox_sdk.http_policy import get_retry_delay_seconds, should_retry_transient_http


class TestHttpPolicy(unittest.TestCase):
  def test_transient_retry_idempotent_only(self) -> None:
    self.assertTrue(should_retry_transient_http("GET", 503))
    self.assertFalse(should_retry_transient_http("POST", 503))
    self.assertFalse(should_retry_transient_http("GET", 404))

  def test_exponential_backoff_with_cap(self) -> None:
    self.assertEqual(get_retry_delay_seconds(1), 0.2)
    self.assertEqual(get_retry_delay_seconds(2), 0.4)
    self.assertEqual(get_retry_delay_seconds(3), 0.8)
    self.assertEqual(get_retry_delay_seconds(4), 1.6)
    self.assertEqual(get_retry_delay_seconds(5), 2.0)
    self.assertEqual(get_retry_delay_seconds(8), 2.0)


if __name__ == "__main__":
  unittest.main()
