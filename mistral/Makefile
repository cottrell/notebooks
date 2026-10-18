all:
	cat Makefile

install:
	curl -LsSf https://mistral.ai/vibe/install.sh | bash

update:
	vibe update

LOAD_ENV = [ -f ~/.cred/ai.sh ] && . ~/.cred/ai.sh;

# Free experimenter tier key: https://console.mistral.ai/api-keys
# Dedicated coding model with FIM:
aider:
	@$(LOAD_ENV) \
	if [ -z "$$MISTRAL_API_KEY" ]; then echo "Missing MISTRAL_API_KEY in environment or ~/.cred/ai.sh"; exit 1; fi; \
	aider --model mistral/codestral-latest

aichat:
	@$(LOAD_ENV) \
	if [ -z "$$MISTRAL_API_KEY" ]; then echo "Missing MISTRAL_API_KEY in environment or ~/.cred/ai.sh"; exit 1; fi; \
	aichat -m mistral:codestral-latest