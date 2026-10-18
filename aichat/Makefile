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
