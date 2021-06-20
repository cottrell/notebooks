all:
	cat Makefile

install:
	sudo apt-get update
	sudo apt-get install nginx

get_cert:
	cd /etc/nginx
	sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt

edit_config:
	sudo vi /etc/nginx/sites-enabled/default
