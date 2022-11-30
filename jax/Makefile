all:
	cat Makefile

install:
	# from https://github.com/google/jax circa 2022-11
	pip install --upgrade pip
	pip install --upgrade "jax[cuda]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

test:
	TF_CPP_MIN_LOG_LEVEL=0 ./check_gpu.py
