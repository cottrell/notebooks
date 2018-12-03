#!/bin/sh -e
cd ~/dev
[ -d Horizon ] || git clone https://github.com/facebookresearch/Horizon.git
cd Horizon

if [ "$1" = "local" ]; then
    pip install onnx

    # put this somewhere
    export JAVA_HOME="$(dirname $(dirname -- `which conda`))"

    # install spark and include in path (see ../spark/down...sh

    pip install "gym[classic_control,box2d,atari]"
    thrift --gen py --out . ml/rl/thrift/core.thrift
elif [ "$1" = "docker_gpu" ]; then
    echo docker
    docker run --runtime=nvidia -v $PWD/../:/home/Horizon -p 0.0.0.0:6006:6006 -it horizon:dev
else
    echo dunno
    exit 1
fi

