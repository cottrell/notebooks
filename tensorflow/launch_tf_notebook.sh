#!/bin/sh
docker run --runtime=nvidia -it -p 8888:8888 tensorflow/tensorflow:latest-gpu
