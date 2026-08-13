all:
	cat Makefile

install:
	echo "WARNING: you should really review this script and not just install blindly ..."
	sleep 3
	curl -sSf https://radicle.dev/install | sh

install-desktop:
	echo "WARNING: you should really review this script and not just install blindly ..."
	sleep 3
	curl -LO https://radicle.dev/apt/radicle-archive-keyring.deb && chmod a+r radicle-archive-keyring.deb && sudo apt install ./radicle-archive-keyring.deb && echo "deb [signed-by=/usr/share/radicle/radicle-archive-keyring.asc] https://radicle.dev/apt release main" | sudo tee /etc/apt/sources.list.d/radicle.list && sudo apt update && sudo apt install radicle-desktop
