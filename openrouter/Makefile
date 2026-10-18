all:
	cat Makefile

LOAD_ENV = [ -f ~/.cred/ai.sh ] && . ~/.cred/ai.sh;

# Inspect live free models:
list-free:
	curl -s https://openrouter.ai/api/v1/models | jq -r '.data[] | select(.id | endswith(":free")) | .id'

# Test API connection with OPENROUTER_API_KEY:
test:
	@$(LOAD_ENV) \
	if [ -z "$$OPENROUTER_API_KEY" ]; then echo "Missing OPENROUTER_API_KEY in environment or ~/.cred/ai.sh"; exit 1; fi; \
	curl -s https://openrouter.ai/api/v1/chat/completions \
	  -H "Authorization: Bearer $$OPENROUTER_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "cohere/north-mini-code:free", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

# Free pool model reminders:
# - openrouter/cohere/north-mini-code:free (verified live)
# - openrouter/deepseek/deepseek-r1:free
# - openrouter/google/gemma-4-31b-it:free

aider-code:
	@$(LOAD_ENV) aider --model openrouter/cohere/north-mini-code:free

aider-r1:
	@$(LOAD_ENV) aider --model openrouter/deepseek/deepseek-r1:free
