#!/bin/bash
MY_CONDA_ENV=A
# PYTHON_ENV=3
PYTHON_ENV=3.11
conda create -c conda-forge -y -n $MY_CONDA_ENV python=PYTHON_ENV
pip install -U pip
pip install -U gpytorch
