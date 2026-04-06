import os

from ai_sandbox_sdk import AiSandboxClient

client = AiSandboxClient(
    base_url=os.getenv("AI_SANDBOX_BASE_URL", "https://www.egroupai.com"),
    api_key=os.getenv("AI_SANDBOX_API_KEY", ""),
)

result = client.create_agent({
    "agentDisplayName": "Python SDK Quickstart",
    "agentDescription": "Created by Python SDK",
})
print(result)
