#!/bin/sh
docker run --runtime=nvidia -p 8888:8888 -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow:latest-gpu-py3 $@
