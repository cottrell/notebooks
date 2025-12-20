all:
	cat Makefile


llama_install_gpu:
	# Install CUDA toolkit
	sudo apt install nvidia-cuda-toolkit
	# Reinstall llama-cpp-python with CUDA support
	CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir


llama_install_cpu:
	uv pip install llama-cpp-python

test:
	python test.py

