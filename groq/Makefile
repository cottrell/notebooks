all:
	cat Makefile

install:
	uv tool install groq-cli
	@echo "Installed groq CLI as 'grc'"

update:
	uv tool upgrade groq-cli

uninstall:
	uv tool uninstall groq-cli

# Test API connection with GROQ_API_KEY:
test:
	@if [ -z "$$GROQ_API_KEY" ]; then echo "Missing GROQ_API_KEY. Grab from https://console.groq.com/keys"; exit 1; fi
	curl -s https://api.groq.com/openai/v1/chat/completions \
	  -H "Authorization: Bearer $$GROQ_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

# Model reminders:
# - llama-3.3-70b-versatile : Fast general purpose / architecture
# - qwen-2.5-coder-32b      : Dedicated coding model
# - deepseek-r1-distill-llama-70b : Reasoning / thinking model

aider-llama:
	aider --model groq/llama-3.3-70b-versatile

aider-qwen:
	aider --model groq/qwen-2.5-coder-32b

aider-reasoning:
	aider --model groq/deepseek-r1-distill-llama-70b

aichat-llama:
	aichat -m groq:llama-3.3-70b-versatile
