all:
	cat Makefile

build:
	docker build . -t books:latest

run:
	docker run -v ~/syncthing/reading/books:/app/books -p 8124:8124 -it books:latest 8124

exec:
	docker run -it --entrypoint /bin/sh books:latest
