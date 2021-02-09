all:
	cat Makefile

list-all:
	systemctl list-unit-files --type=service
	# ls /lib/systemd/system/*.service /etc/systemd/system/*.service

list-units:
	systemctl list-units --type=service

reset-failed:
	systemctl reset-failed

# disable via: systemctl disable SERVICE
# stop/start via: service SERVICE start/stop
