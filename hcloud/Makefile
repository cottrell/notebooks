all:
	@cat Makefile

install:
	# Official repo: https://github.com/hetznercloud/cli
	# Quick install via apt:
	# sudo apt install hcloud-cli
	# Or via brew:
	# brew install hcloud
	# Or manual release binary:
	# curl -fsSL https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz | tar -xz -C /usr/local/bin hcloud
	sudo apt-get update && sudo apt-get install -y hcloud-cli

install-bin:
	curl -fsSL https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz | tar -xz hcloud
	mkdir -p ~/bin ~/.local/bin
	mv hcloud ~/.local/bin/

version:
	hcloud version

init:
	# Setup API token context
	hcloud context create default

server-list:
	hcloud server list
