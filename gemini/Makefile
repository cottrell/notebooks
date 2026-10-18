all:
	cat Makefile

install:
	bun install -g @google/gemini-cli
	@echo "Installed gemini CLI"

update:
	bun install -g @google/gemini-cli@latest

uninstall:
	bun uninstall -g @google/gemini-cli

# Automatically load from ~/.cred/ai.sh if not exported in current shell:
LOAD_ENV = [ -f ~/.cred/ai.sh ] && . ~/.cred/ai.sh;

# Test API connection with GEMINI_API_KEY:
test:
	@$(LOAD_ENV) \
	if [ -z "$$GEMINI_API_KEY" ]; then echo "Missing GEMINI_API_KEY in environment or ~/.cred/ai.sh"; exit 1; fi; \
	curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=$$GEMINI_API_KEY" \
	  -H 'Content-Type: application/json' \
	  -d '{"contents":[{"parts":[{"text":"ping"}]}]}' | jq -r '.candidates[0].content.parts[0].text'

# Agentic coding with aider (free 1,500 req/day quota):
aider:
	@$(LOAD_ENV) aider --model gemini/gemini-3.8-flash

# TUI scratchpad with aichat:
aichat:
	@$(LOAD_ENV) aichat -m gemini:gemini-3.8-flash
