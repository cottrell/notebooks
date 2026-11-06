.PHONY: all install install-script update update-script status version

all:
	@cat Makefile

install:
	sudo apt update && sudo apt install -y ghostty

install-script:
	/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/mkasberg/ghostty-ubuntu/HEAD/install.sh)"

update:
	sudo apt update && sudo apt install --only-upgrade -y ghostty

update-script:
	/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/mkasberg/ghostty-ubuntu/HEAD/install.sh)"

status:
	@apt-cache policy ghostty
	@which ghostty || true

version:
	@ghostty --version
