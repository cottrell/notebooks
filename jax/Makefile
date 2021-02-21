all:
	cat Makefile

install:
	pip install --upgrade jax
	# 0.1.61 was latest jaxlib and cuda112 and 11.2 see nvcc --version
	pip install --upgrade jax jaxlib==0.1.61+cuda112 -f https://storage.googleapis.com/jax-releases/jax_releases.html

test:
	./check_gpu.py
