#!/bin/bash -e
source ~/anaconda3/etc/profile.d/conda.sh
MY_CONDA_ENV=tf
PYTHON_ENV=3.12
if [[ $(conda env list | grep $MY_CONDA_ENV"\s") ]]; then
    echo CONDA ENV $MY_CONDA_ENV exists
else
    echo CONDA ENV $MY_CONDA_ENV does not exist
    # conda create -c conda-forge -y -n $MY_CONDA_ENV python=$MY_CONDA_ENV
    conda create -y -n $MY_CONDA_ENV python=$PYTHON_ENV
    conda init
    conda activate $MY_CONDA_ENV
    conda install -y pip
fi
conda init
conda activate $MY_CONDA_ENV
conda info
sleep 1
pip install -U pip

pip install -r ./requirements_tf.txt
./local_setup.sh
