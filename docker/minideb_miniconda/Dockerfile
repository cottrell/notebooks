FROM bitnami/minideb:latest

RUN apt-get update
RUN apt-get install -y wget curl bzip2
ENV PATH="/root/minconda3/bin:${PATH}"
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash ./Miniconda3-latest-Linux-x86_64.sh -b
RUN /root/minconda3/bin/conda install -y python=3.6
