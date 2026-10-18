all:
	cat Makefile

install:
	bun install -g openrouter-cli
	@echo "Installed openrouter CLI as 'openrouter'"

update:
	bun install -g openrouter-cli@latest

uninstall:
	bun uninstall -g openrouter-cli

# OpenRouter provides a zero-dollar pool of models tagged with :free
# Key signup: https://openrouter.ai/keys

list-free:
	curl -s https://openrouter.ai/api/v1/models | jq -r '.data[] | select(.id | endswith(":free")) | .id'

test:
	@if [ -z "$$OPENROUTER_API_KEY" ]; then echo "Missing OPENROUTER_API_KEY. Grab from https://openrouter.ai/keys"; exit 1; fi
	curl -s https://openrouter.ai/api/v1/chat/completions \
	  -H "Authorization: Bearer $$OPENROUTER_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "google/gemma-4-31b-it:free", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

# Free pool model reminders:
# - openrouter/deepseek/deepseek-r1:free
# - openrouter/meta-llama/llama-3.3-70b-instruct:free
# - openrouter/cohere/north-mini-code:free

aider-r1:
	aider --model openrouter/deepseek/deepseek-r1:free

aider-llama:
	aider --model openrouter/meta-llama/llama-3.3-70b-instruct:free
