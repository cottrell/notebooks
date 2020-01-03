SHELL := /bin/bash

build:
	mkdir -p cache
	[[ -e "cache/kafka_2.12-2.4.0.tgz" ]] && echo tgz exists || wget http://apache.mirror.anlx.net/kafka/2.4.0/kafka_2.12-2.4.0.tgz -P cache
	[[ -e "cache/kafka_2.12-2.4.0" ]] && echo dir exists || { cd cache && tar -xzf kafka_2.12-2.4.0.tgz; }
	DOCKER_BUILDKIT=1 docker build . --tag kafka:latest

start:
	docker stop kafka || true && docker rm kafka || true
	docker run --name=kafka -P -t kafka:latest || docker start kafka

stop:
	docker exec kafka kafka_2.12-2.4.0/bin/zookeeper-server-stop.sh
	docker exec kafka kafka_2.12-2.4.0/bin/kafka-server-stop.sh
	docker stop kafka

bash:
	docker run -it kafka:latest /bin/bash

all:
	build

