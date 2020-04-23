#!/bin/bash
pattern="tensorflow/tensorflow:latest-gpu"
if [[ $(docker ps | grep $pattern | wc -l) -ne 1 ]]; then
    echo got multiple matches for container:
    docker ps | grep $pattern
    exit 1
fi
ID=$(docker ps | grep $pattern | cut -d' ' -f1)

docker exec -it $ID /bin/bash
