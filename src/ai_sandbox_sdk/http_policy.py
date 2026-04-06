from __future__ import annotations


def should_retry_transient_http(method: str, status: int) -> bool:
  """僅對 GET/HEAD 在 429 或 5xx 時建議重試，避免寫入重複副作用。"""
  if status != 429 and not (500 <= status <= 599):
    return False
  m = (method or "").strip().upper()
  return m in ("GET", "HEAD")
