#!/bin/bash -e
# use this to build AMI or local machine state
# extremely fragile, likely doesn't complete, baby it along
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

type gcc || echo no gcc installed!

if [[ $(uname) != "Darwin" ]]; then
    sudo apt-get install -y libffi-dev
    sudo apt-get install -y graphviz
    sudo apt-get install -y git-lfs
    sudo apt-get install -y ccache
else
    type wget || brew install wget
    type graphviz || brew install graphviz
    type git-lfs || brew install git-lfs
    brew upgrade graphviz
    brew upgrade git-lfs
fi

# https://repo.anaconda.com/archive
function install_conda() {
    if [[ $(uname) = "Linux" ]]; then
        # filename=Anaconda3-2019.10-Linux-x86_64.sh
        filename=Anaconda3-2020.02-Linux-x86_64.sh
    else
        filename=Anaconda3-2020.02-MacOSX-x86_64.sh
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

MY_CONDA_ENV=39

if [[ $(conda env list | grep $MY_CONDA_ENV"\s") ]]; then
    echo CONDA ENV $MY_CONDA_ENV exists
else
    echo CONDA ENV $MY_CONDA_ENV does not exist
    conda create -y -n $MY_CONDA_ENV python=3.9
    conda activate $MY_CONDA_ENV
    conda install -y pip
fi
conda activate $MY_CONDA_ENV
pip install -U pip

if [[ $(uname) = "Darwin" ]]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    brew update && brew upgrade
    brew install openssl
fi

$DIR/upgrade.sh

$DIR/local_setup.sh
