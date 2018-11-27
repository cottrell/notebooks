# Setup

Installing on newer OS and drivers is tricky but might eventually be worth it.

Using docker is likely easier, even for experimenting rolling your own build.

See nvidia_docker for setting up docker.


# Docker examples

    # test with this
    docker run --runtime=nvidia -it -p 8888:8888 tensorflow/tensorflow:latest-gpu

See ~/dev/tensorflow/tensorflow/examples

    docker pull tensorflow/tensorflow
