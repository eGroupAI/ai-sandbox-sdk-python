# Integration Guide (Python)

This SDK is designed for low-change, low-touch customer integration.

## Goals
- Stable API surface for v1.
- Explicit timeout and retry controls.
- Streaming chat support (`text/event-stream`).

## Retry safety
- **429 / 5xx** automatic retries apply only to **GET** and **HEAD**. **POST / PUT / PATCH** are not retried on those status codes to avoid duplicate side effects.
- **Network** errors (`requests.RequestException`) may still be retried for all methods, up to `max_retries`.

## Install
`pip install ai-sandbox-sdk-python`

## First Steps
1. Configure `base_url` and `api_key` on `AiSandboxClient`.
2. Call `create_agent(...)`.
3. Create a chat channel with `create_chat_channel(...)` and send the first message with `send_chat(...)` or `send_chat_stream(...)`.
