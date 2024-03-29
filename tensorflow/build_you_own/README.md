# Setup

Installing on newer OS and drivers is tricky but might eventually be worth it.

Using docker is likely easier, even for experimenting rolling your own build.

See nvidia_docker for setting up docker.


# Docker examples

    # test with this
    docker run --runtime=nvidia -it -p 8888:8888 tensorflow/tensorflow:latest-gpu

See ~/dev/tensorflow/tensorflow/examples

    docker pull tensorflow/tensorflow

If you paste the check_gpu.py script in a notebook you can see output in the logs not the notebook.

See the Dockerfiles https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/docker

# Workflow

Spin up a docker container. Work on the files in the docker volume on the host using whatever you want. Iterate in a ssh window or notebook. Not too bad.
