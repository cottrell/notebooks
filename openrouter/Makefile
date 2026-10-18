all:
	cat Makefile

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
