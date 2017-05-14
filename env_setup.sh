#!/bin/sh

if [[ "$#" -ne 1 ]]; then
    echo usage: prog env
    exit 1
fi

ENV=$1

if [[ ! $(conda info --envs | grep $ENV) ]]; then
    echo "conda info --envs did not return env $ENV. quitting."
    echo "run: conda create -n $ENV python=<python version>"
    exit 1
fi

source activate $ENV || exit 1
pip install ipython # see issue https://github.com/ipython/ipython/issues/10560
conda install -y pandas anaconda-client scikit-learn matplotlib jupyter dask
conda install -y keras jupyterhub -c conda-forge
pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.1.0-py3-none-any.whl
