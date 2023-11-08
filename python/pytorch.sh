#!/bin/bash -e
MY_CONDA_ENV=pytorch
# PYTHON_ENV=3
PYTHON_ENV=3.11
conda create -c conda-forge -y -n $MY_CONDA_ENV python=$PYTHON_ENV
echo conda activate $MY_CONDA_ENV
echo pip install -U pip
echo pip install -U gpytorch
