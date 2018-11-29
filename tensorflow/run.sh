#!/bin/sh
docker run --runtime=nvidia -it --rm -v $PWD:/root/stuff -w /root tensorflow/tensorflow:latest-gpu-py3 $@
