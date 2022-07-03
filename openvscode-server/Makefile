all:
	cat Makefile
docker:
	docker run -it --init -p 3000:3000 -v "$(pwd):/home/workspace:cached" gitpod/openvscode-server

download:
	wget https://github.com/gitpod-io/openvscode-server/releases/download/openvscode-server-v1.68.1/openvscode-server-v1.68.1-linux-x64.tar.gz
	tar xzf openvscode-server-v1.68.1-linux-x64.tar.gz

run:
	./openvscode-server-v1.68.1-linux-x64/bin/openvscode-server --port 8778
