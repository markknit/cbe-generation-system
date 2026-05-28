from anthropic import Anthropic

client = Anthropic(api_key="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")

print("Testing Anthropic API...")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello"}]
)

print("✓ API works!")
print(f"Response: {response.content[0].text}")
