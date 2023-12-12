all:
	cat Makefile

install:
	sudo apt-get install tor
	#
	pip install stem  # for identity requesting
	pip install fake_useragent
	# you must also add these to file:
	# sudo vi /etc/tor/torrc
	# ControlPort 9051
	# CookieAuthentication 1
	# DataDirectoryGroupReadable 1
	# CookieAuthFileGroupReadable 1
	# ExtORPortCookieAuthFileGroupReadable 1
	# CacheDirectoryGroupReadable 1


start:
	sudo service tor start

stop:
	sudo service tor stop

restart:
	sudo service tor restart

fix_bug:
	sudo chmod 777 /run/tor/control.authcookie

test:
	curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs
	# THIS LINE IS JUST AN EXAMPLE NOT A RESULT (the result is above, missing means failure): success looks like: Congratulations. This browser is configured to use Tor.

test_python:
	python ./test.py

test_stem:
	python ./test_stem.py

make_torfiles:
	sudo /home/cottrell/anaconda3/envs/38/bin/python ./make_torfiles.py -n 5

start_many:
	sudo ./start_many.sh

stop_many:
	sudo ./stop_many.sh
