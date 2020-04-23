Look first at these: https://hub.docker.com/r/nvidia/cuda/

https://hub.docker.com/r/nvidia/cuda/
https://gitlab.com/nvidia/cuda/blob/ubuntu18.04/9.2/base/Dockerfile
https://gitlab.com/nvidia/cuda/blob/ubuntu18.04/9.2/runtime/Dockerfile
https://gitlab.com/nvidia/cuda/blob/ubuntu18.04/9.2/runtime/cudnn7/Dockerfile
https://gitlab.com/nvidia/cuda/blob/ubuntu18.04/9.2/devel/cudnn7/Dockerfile


Swap out the nvidia stuff in the tensorflow and see if it works.

The devel are for building.
