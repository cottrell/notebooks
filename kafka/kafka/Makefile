SHELL := /bin/bash

all: build

wget:
	mkdir -p cache
	[[ -e "cache/kafka_2.12-2.4.0.tgz" ]] && echo tgz exists || wget http://apache.mirror.anlx.net/kafka/2.4.0/kafka_2.12-2.4.0.tgz -P cache
	[[ -e "cache/kafka_2.12-2.4.0" ]] && echo dir exists || { cd cache && tar -xzf kafka_2.12-2.4.0.tgz; }

build_zookeeper: wget
	cp -R cache zookeeper
	cd zookeeper && DOCKER_BUILDKIT=1 docker build . --tag zookeeper:latest
	rm -rf zookeeper/cache

build_kafka: wget
	cp -R cache kafka
	cd kafka && DOCKER_BUILDKIT=1 docker build . --tag kafka:latest
	rm -rf kafka/cache

build: build_zookeeper build_kafka

start:
	docker stop zookeeper || true && docker rm zookeeper || true
	docker stop kafka || true && docker rm kafka || true
	docker run --name=zookeeper -p "2181:2181" -t zookeeper:latest || docker start zookeeper
	docker run --network=host --name=kafka -p "9092:9092" -t kafka:latest || docker start kafka

stop:
	docker exec kafka kafka_2.12-2.4.0/bin/kafka-server-stop.sh
	docker exec kafka kafka_2.12-2.4.0/bin/zookeeper-server-stop.sh
	docker stop kafka

bash:
	docker run -it kafka:latest /bin/bash

ssh:
	docker exec -it kafka /bin/bash

port:
	docker port kafka
