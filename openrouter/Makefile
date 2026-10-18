all:
	cat Makefile

# OpenRouter is a unified API gateway (not a local tool / CLI to install).
# It provides a pool of models tagged with :free at $0.00 / 1M tokens.
# Free API key: https://openrouter.ai/keys

# Inspect live free models:
list-free:
	curl -s https://openrouter.ai/api/v1/models | jq -r '.data[] | select(.id | endswith(":free")) | .id'

# Test API connection with OPENROUTER_API_KEY:
test:
	@if [ -z "$$OPENROUTER_API_KEY" ]; then echo "Missing OPENROUTER_API_KEY. Grab from https://openrouter.ai/keys"; exit 1; fi
	curl -s https://openrouter.ai/api/v1/chat/completions \
	  -H "Authorization: Bearer $$OPENROUTER_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "google/gemma-4-31b-it:free", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

# Model reminders for coding harnesses (aider):
# - openrouter/deepseek/deepseek-r1:free
# - openrouter/meta-llama/llama-3.3-70b-instruct:free
# - openrouter/cohere/north-mini-code:free

aider-r1:
	aider --model openrouter/deepseek/deepseek-r1:free

aider-llama:
	aider --model openrouter/meta-llama/llama-3.3-70b-instruct:free
