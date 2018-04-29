# FROM python:3.6-alpine
# https://github.com/docker-library/python/blob/b99b66406ebe728fb4da64548066ad0be6582e08/3.6/alpine3.6/Dockerfile
FROM centos:centos7
RUN yum -y update
RUN yum -y install yum-utils
RUN yum -y groupinstall development
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python36u
RUN yum -y install python36u-pip
RUN yum -y install python36u-devel
RUN pip3.6 install pandas
COPY ./app /app
WORKDIR /app
# RUN pip install -r requirements.txt --no-build-isolation
# CMD ["gunicorn", "-w 4", "main:app"]
