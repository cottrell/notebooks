#!/bin/sh
# stateless
# docker run --runtime=nvidia -it -p 8888:8888 tensorflow/tensorflow:latest-gpu

# with bind mounted volume
vol="./docker_volume"
if [ "$1" ]; then
    vol=$1
fi
vol=$(realpath $vol)
# make it otherwise root owns it
mkdir -p $vol
echo docker run --runtime=nvidia -it -p 8888:8888 -v $vol:/tmp --rm --name tf_notebook tensorflow/tensorflow:latest-gpu
docker run --runtime=nvidia -it -p 8888:8888 -v $vol:/tmp --rm --name tf_notebook tensorflow/tensorflow:latest-gpu
