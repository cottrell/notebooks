#!/bin/bash -e
# use this to build AMI or local machine state
# extremely fragile, likely doesn't complete, baby it along
# see setup_darwin.sh and setup_debian.sh
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

type gcc || echo no gcc installed!

# https://repo.anaconda.com/archive
function install_conda() {
    if [[ $(uname) = "Linux" ]]; then
        filename=Anaconda3-2022.10-Linux-x86_64.sh
    else
        filename=Anaconda3-2022.10-MacOSX-x86_64.sh
    fi
    echo Will install: $filename

    cd /var/tmp
    if [[ -e $filename ]]; then
        echo $filename exists
    else
        wget https://repo.anaconda.com/archive/$filename
    fi

    [[ -e ~/anaconda3 ]] || bash ./$filename -b -u
}

type conda || install_conda

source ~/anaconda3/etc/profile.d/conda.sh

conda update -y -n base -c defaults conda

# MY_CONDA_ENV=39
MY_CONDA_ENV=3.10.4
# MY_CONDA_ENV=3.11.0

if [[ $(conda env list | grep $MY_CONDA_ENV"\s") ]]; then
    echo CONDA ENV $MY_CONDA_ENV exists
else
    echo CONDA ENV $MY_CONDA_ENV does not exist
    # conda create -y -n $MY_CONDA_ENV python=3.9
    # conda create -y -n $MY_CONDA_ENV python=$MY_CONDA_ENV
    # NOTE: needed conda forge for 3.11
    conda create -c conda-forge -y -n $MY_CONDA_ENV python=$MY_CONDA_ENV
    conda activate $MY_CONDA_ENV
    conda install -y pip
fi
conda activate $MY_CONDA_ENV
pip install -U pip

$DIR/upgrade.sh

$DIR/local_setup.sh
