#!/bin/sh
docker run --runtime=nvidia -it --rm -v $PWD:/root -w /root tensorflow/tensorflow:latest-gpu-py3 $@
