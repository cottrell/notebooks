#!/bin/sh
docker run --runtime=nvidia -it --rm -v $PWD:/tmp -w /tmp tensorflow/tensorflow:latest-gpu-py3 $@
