all:
	cat Makefile

install:
	# LiteLLM: Proxy for LLM APIs (OpenAI, Anthropic, Gemini, etc.)
	# Using uv for installation as per project convention
	uv pip install 'litellm[proxy]'

run:
	# Start the proxy server
	litellm --model gpt-3.5-turbo
