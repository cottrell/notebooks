#!/bin/sh
docker run --runtime=nvidia -v $PWD/../:/home/Horizon -p 0.0.0.0:6006:6006 -it horizon:dev

