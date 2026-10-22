.PHONY: all help install update

PYTHON ?= python
UV ?= uv

all help:
	@cat Makefile

install:
	$(UV) pip install ray

update:
	$(UV) pip install --upgrade ray
