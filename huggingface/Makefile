.PHONY: install install-fast login download list-models run-model create-model remove-model

all:
	cat Makefile

install:
	pip install -U huggingface-hub

install-fast:
	pip install -U huggingface-hub hf-transfer
	echo 'export HUGGINGFACE_HUB_ENABLE_HF_TRANSFER=1' >> ~/.bashrc
	echo 'export HF_HUB_ENABLE_HF_TRANSFER=1' >> ~/.bashrc

login:
	hf auth login

download:
	hf download $(repo) --local-dir $(dir)
