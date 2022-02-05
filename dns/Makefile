all:
	cat Makefile

view:
	systemd-resolve --status

test:
	dig +trace www.stackoverflow.com

clear:
	sudo /etc/init.d/networking restart
	# uname osx
	# sudo killall -HUP mDNSResponder

restart:
	sudo service resolvconf restart
	cat /etc/resolv.conf


ping:
	ping dsldevice.lan

nmcli_show:
	nmcli show
