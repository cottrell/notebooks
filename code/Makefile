all:
	cat Makefile

install_code:
	echo DOWNLOAD DEB AND INSTALL MANUALLY

install_code_server:
	curl -fsSL https://code-server.dev/install.sh | sh
	echo remember to see README for enable etc for first time setup

status:
	systemctl status code-server@$$USER

start:
	sudo systemctl start code-server@$$USER

stop:
	sudo systemctl stop code-server@$$USER

bounce:
	sudo systemctl restart code-server@$$USER.service

run:
	code-server --bind-addr 0.0.0.0:8080
