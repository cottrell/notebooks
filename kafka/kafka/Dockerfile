# syntax=docker/dockerfile:experimental

FROM ubuntu:18.04
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
RUN apt-get update -y
RUN apt-get install -y wget

RUN --mount=type=bind,source=./cache,target=/tmp/cache tar -xzf /tmp/cache/kafka_2.12-2.4.0.tgz
RUN --mount=type=cache,target=/tmp/cache apt install -y default-jdk

CMD cd kafka_2.12-2.4.0 && bin/zookeeper-server-start.sh config/zookeeper.properties & cd kafka_2.12-2.4.0 && bin/kafka-server-start.sh config/server.properties
EXPOSE 9092
