all:
	cat Makefile

install:
	curl -LsSf https://mistral.ai/vibe/install.sh | bash

update:
	vibe update

# Free experimenter tier key: https://console.mistral.ai/api-keys
# Dedicated coding model with FIM:
aider:
	@if [ -z "$$MISTRAL_API_KEY" ]; then echo "Missing MISTRAL_API_KEY. Grab from https://console.mistral.ai/api-keys"; exit 1; fi
	aider --model mistral/codestral-latest

aichat:
	@if [ -z "$$MISTRAL_API_KEY" ]; then echo "Missing MISTRAL_API_KEY. Grab from https://console.mistral.ai/api-keys"; exit 1; fi
	aichat -m mistral:codestral-latest