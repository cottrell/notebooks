all:
	cat Makefile

install:
	curl -sL https://github.com/sigoden/aichat/releases/latest/download/aichat-$$(curl -sL https://api.github.com/repos/sigoden/aichat/releases/latest | jq -r .tag_name)-x86_64-unknown-linux-musl.tar.gz | tar -xz -C ~/.local/bin aichat
	chmod +x ~/.local/bin/aichat
	@echo "Installed aichat to ~/.local/bin/aichat"
	~/.local/bin/aichat --version

update: install

uninstall:
	rm -f ~/.local/bin/aichat

# Usage & model reminders:
# Config location: ~/.config/aichat/config.yaml

# Interactive REPL / TUI:
repl:
	aichat

# Direct scratchpad queries using specific free endpoints:
query-groq:
	@if [ -z "$$GROQ_API_KEY" ]; then echo "Missing GROQ_API_KEY"; exit 1; fi
	aichat -m groq:llama-3.3-70b-versatile "reply pong in one word"

query-mistral:
	@if [ -z "$$MISTRAL_API_KEY" ]; then echo "Missing MISTRAL_API_KEY"; exit 1; fi
	aichat -m mistral:codestral-latest "reply pong in one word"
