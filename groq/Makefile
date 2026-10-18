all:
	cat Makefile

LOAD_ENV = [ -f ~/.cred/ai.sh ] && . ~/.cred/ai.sh;

# Test API connection with GROQ_API_KEY:
test:
	@$(LOAD_ENV) \
	if [ -z "$$GROQ_API_KEY" ]; then echo "Missing GROQ_API_KEY in environment or ~/.cred/ai.sh"; exit 1; fi; \
	curl -s https://api.groq.com/openai/v1/chat/completions \
	  -H "Authorization: Bearer $$GROQ_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "qwen/qwen3.8-27b", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

# Currently active models on Groq:
# - qwen/qwen3.8-27b      : Fast coding & instruction model
# - openai/gpt-oss-120b   : Massive 120B open-weights model
# - openai/gpt-oss-20b    : Lightweight 20B reasoning model

aider-qwen:
	@$(LOAD_ENV) aider --model groq/qwen/qwen3.8-27b

aider-120b:
	@$(LOAD_ENV) aider --model groq/openai/gpt-oss-120b

aichat-qwen:
	@$(LOAD_ENV) aichat -m groq:qwen/qwen3.8-27b
