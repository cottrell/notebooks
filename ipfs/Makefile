all:
	cat Makefile

install:
	./install.sh

reset:
	rm -rvf $HOME/.ipfs
	ipfs init

pip_install:
	pip install ipfshttpclient
	# see my fork for dev install
	# git clone https://github.com/ipfs/py-ipfs-http-client

daemon:
	ipfs daemon
	# see localhost:5001/webui
	# see localhost:8080/ipfs/hash
