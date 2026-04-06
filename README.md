# AI Sandbox SDK for Python

![Motion headline](https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=24&duration=2800&pause=800&color=1F6FEB&background=FFFFFF00&width=900&lines=Design+Fast+and+Beautiful+AI+Workflows;11+APIs+%7C+SSE+Streaming+%7C+GA+v1)

![GA](https://img.shields.io/badge/GA-v1-0A84FF?style=for-the-badge)
![APIs](https://img.shields.io/badge/APIs-11-00A86B?style=for-the-badge)
![Streaming](https://img.shields.io/badge/SSE-Ready-7C3AED?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-SDK-3776AB?style=for-the-badge)

## UX-First Value Cards

| Quick Integration | Real-Time Experience | Reliability by Default |
| --- | --- | --- |
| Minimal setup and low-change onboarding | Streaming chunks via `send_chat_stream(...)` | Built-in timeout and retry controls |

## Visual Integration Flow

```mermaid
flowchart LR
  A[Create Agent] --> B[Create Chat Channel]
  B --> C[Send Message]
  C --> D[SSE Stream Chunks]
  D --> E[Attach Knowledge Base]
  E --> F[Customer-Ready Experience]
```

## 60-Second Quick Start

```python
import os
from ai_sandbox_sdk import AiSandboxClient

client = AiSandboxClient(
    base_url=os.getenv("AI_SANDBOX_BASE_URL", "https://www.egroupai.com"),
    api_key=os.getenv("AI_SANDBOX_API_KEY", ""),
)

agent = client.create_agent({
    "agentDisplayName": "Support Agent",
    "agentDescription": "Handles customer inquiries",
})
agent_id = int(agent["payload"]["agentId"])

channel = client.create_chat_channel(agent_id, {
    "title": "Web Chat",
    "visitorId": "visitor-001",
})
channel_id = channel["payload"]["channelId"]

for chunk in client.send_chat_stream(agent_id, {
    "channelId": channel_id,
    "message": "What is the return policy?",
    "stream": True,
}):
    print(chunk)
```

## Installation

```bash
pip install ai-sandbox-sdk-python
```

## Snapshot

| Metric | Value |
| --- | --- |
| API Coverage | 11 operations (Agent / Chat / Knowledge Base) |
| Stream Mode | `text/event-stream` with `[DONE]` handling |
| Error Surface | `ApiError` with status/body/trace_id |
| Validation | Production-host integration verified |

## Links

- [Official System Integration Docs](https://www.egroupai.com/ai-sandbox/system-integration)
- [30-Day Optimization Plan](docs/30D_OPTIMIZATION_PLAN.md)
- [Integration Guide](docs/INTEGRATION.md)
- [Quickstart Example](examples/quickstart.py)
- [Repository](https://github.com/eGroupAI/ai-sandbox-sdk-python)
