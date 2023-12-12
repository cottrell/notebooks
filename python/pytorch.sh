#!/bin/bash -e
MY_CONDA_ENV=pytorch
# PYTHON_ENV=3
PYTHON_ENV=3.11
conda create -c conda-forge -y -n $MY_CONDA_ENV python=$PYTHON_ENV
conda activate $MY_CONDA_ENV
pip install -U pip
pip install -r ./requirements_pytorch.txt
./local_setup.sh
