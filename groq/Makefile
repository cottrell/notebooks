all:
	cat Makefile

# Groq Cloud provides free tier inference for Llama 3.3, Qwen 2.5 Coder, DeepSeek R1 distill
# Key signup: https://console.groq.com/keys

test:
	@if [ -z "$$GROQ_API_KEY" ]; then echo "Missing GROQ_API_KEY. Grab from https://console.groq.com/keys"; exit 1; fi
	curl -s https://api.groq.com/openai/v1/chat/completions \
	  -H "Authorization: Bearer $$GROQ_API_KEY" \
	  -H "Content-Type: application/json" \
	  -d '{"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "ping"}]}' | jq .choices[0].message.content

aider:
	aider --model groq/llama-3.3-70b-versatile
