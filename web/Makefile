all:
	cat Makefile

init_npm_packages:
	# https://johnpapa.net/node-and-npm-without-sudo/
	# manual: Install Node.js from https://nodejs.org/en/download/
	mkdir -p ~/.npm-packages
	npm config set prefix ~/.npm-packages

update_npm:
	sudo npm install npm -g
