from __future__ import annotations


def should_retry_transient_http(method: str, status: int) -> bool:
  """Retry 429/5xx only for GET/HEAD to avoid duplicate write side effects."""
  if status != 429 and not (500 <= status <= 599):
    return False
  m = (method or "").strip().upper()
  return m in ("GET", "HEAD")


def get_retry_delay_seconds(attempt: int) -> float:
  safe_attempt = max(1, attempt)
  delay = 0.2 * (2 ** (safe_attempt - 1))
  return min(2.0, delay)
