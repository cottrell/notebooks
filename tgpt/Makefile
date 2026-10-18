all:
	cat Makefile

install:
	curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s ~/.local/bin

update:
	@current_ver=$$(~/.local/bin/tgpt -v 2>/dev/null | awk '{print $$2}' || echo "none"); \
	latest_ver=$$(curl -sI https://github.com/aandrew-me/tgpt/releases/latest | grep -i location | sed -E 's/.*tag\/v?([0-9.]+).*/\1/' | tr -d '\r\n'); \
	if [ "$$current_ver" = "$$latest_ver" ]; then \
		echo "tgpt is already up to date ($$current_ver)"; \
	else \
		echo "Updating tgpt: $$current_ver -> $$latest_ver"; \
		curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s ~/.local/bin; \
	fi

uninstall:
	rm -f ~/.local/bin/tgpt

# Zero-key tests & reminders:
# Default provider (opencode) requires their app. Use --provider pollinations for zero-config free queries:

test:
	tgpt --provider pollinations "reply pong in one word"

# Interactive TUI mode:
interactive:
	tgpt --provider pollinations -i

# Image generation (saved to /tmp/test.jpg):
test-img:
	tgpt --img --out /tmp/tgpt_test.jpg "retro robot reading code"
	@echo "Saved image to /tmp/tgpt_test.jpg"
