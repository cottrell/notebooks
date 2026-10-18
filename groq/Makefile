all:
	cat Makefile

# Groq Cloud is a hosted API service on fast LPU hardware.
# Key signup: https://console.groq.com/keys

# Test API connection with GROQ_API_KEY:
test:
	@if [ -z "$$GROQ_API_KEY" ]; then echo "Missing GROQ_API_KEY. Grab from https://console.groq.com/keys"; exit 1; fi
	curl -s https://api.groq.com/openai/v1/chat/completions \
	  -H "Authorization: Bearer $$GROQ_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "qwen/qwen3.8-27b", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

# Currently active models on Groq:
# - qwen/qwen3.8-27b      : Fast coding & instruction model
# - openai/gpt-oss-120b   : Massive 120B open-weights model
# - openai/gpt-oss-20b    : Lightweight 20B reasoning model

aider-qwen:
	aider --model groq/qwen/qwen3.8-27b

aider-120b:
	aider --model groq/openai/gpt-oss-120b

aichat-qwen:
	aichat -m groq:qwen/qwen3.8-27b
