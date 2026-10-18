all:
	cat Makefile

# Groq Cloud is a hosted API service (not a local tool / CLI to install).
# It serves Llama 3.3 70B, Qwen 2.5 Coder, and DeepSeek R1 distill for free.
# Free API key: https://console.groq.com/keys

# Test API connection with GROQ_API_KEY:
test:
	@if [ -z "$$GROQ_API_KEY" ]; then echo "Missing GROQ_API_KEY. Grab from https://console.groq.com/keys"; exit 1; fi
	curl -s https://api.groq.com/openai/v1/chat/completions \
	  -H "Authorization: Bearer $$GROQ_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

# Model reminders for harnesses (aider / aichat):
# - llama-3.3-70b-versatile : Fast general purpose
# - qwen-2.5-coder-32b      : Dedicated coding model
# - deepseek-r1-distill-llama-70b : Reasoning model

aider-llama:
	aider --model groq/llama-3.3-70b-versatile

aider-qwen:
	aider --model groq/qwen-2.5-coder-32b

aider-reasoning:
	aider --model groq/deepseek-r1-distill-llama-70b

aichat-llama:
	aichat -m groq:llama-3.3-70b-versatile
