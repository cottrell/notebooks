all:
	cat Makefile

install:
	pip install --upgrade jax
	# 0.1.61 was latest jaxlib and cuda112 and 11.2 see nvcc --version
	# pip install --upgrade jax jaxlib==0.1.61+cuda112 -f https://storage.googleapis.com/jax-releases/jax_releases.html
	# 2021-06 says to use cuda111 for all cuda 11.1 and beyond
	pip install --upgrade jax[cuda111] -f https://storage.googleapis.com/jax-releases/jax_releases.html


test:
	TF_CPP_MIN_LOG_LEVEL=0 ./check_gpu.py
