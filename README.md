# AI Sandbox SDK for Python

Official Python SDK for AI Sandbox v1.

## Installation
```bash
pip install ai-sandbox-sdk-python
```

## Quick Start
```python
from ai_sandbox_sdk import AiSandboxClient

client = AiSandboxClient(
  base_url="https://www.egroupai.com",
  api_key="<YOUR_API_KEY>",
)

agent = client.create_agent({
  "agentDisplayName": "Customer Support"
})
```

## Repository
https://github.com/eGroupAI/ai-sandbox-sdk-python
