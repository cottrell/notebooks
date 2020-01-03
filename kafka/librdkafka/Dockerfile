# https://docs.confluent.io/current/installation/installing_cp/deb-ubuntu.html#get-the-software

FROM ubuntu:18.04
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
RUN apt-get update -y && \
    apt-get install -y wget gnupg2 software-properties-common && \
    wget -qO - https://packages.confluent.io/deb/5.3/archive.key | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/5.3 stable main" && \
    apt-get update -y && \
    apt-get install -y confluent-community-2.12 && \
    apt install -y librdkafka-dev
