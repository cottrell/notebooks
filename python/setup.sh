#!/bin/bash -e
# use this to build AMI or local machine state
# extremely fragile, likely doesn't complete, baby it along
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

type gcc || echo no gcc installed!

# https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
function install_conda() {
    if [[ $(uname) = "Linux" ]]; then
        # filename=Anaconda3-5.3.1-Linux-x86_64.sh
        # filename=Anaconda3-2019.07-Linux-x86_64.sh
        filename=Anaconda3-2019.10-Linux-x86_64.sh
    else
        filename=Anaconda3-2019.10-MacOSX-x86_64.sh
    fi
    echo Will install: $filename

    cd /tmp
    if [[ -e $filename ]]; then
        echo $filename exists
    else
        wget https://repo.anaconda.com/archive/$filename
    fi

    [[ -e ~/anaconda3 ]] || bash ./$filename -b -u
}

type conda || install_conda

source ~/anaconda3/etc/profile.d/conda.sh

conda update -n base -c defaults conda

if [[ $(conda env list | grep 37) ]]; then
    echo env probably exists
else
    echo env does not exist
    conda create -n 37 python=3.7
    conda activate 37
    conda install pip
fi
if [[ $(uname) != "Darwin" ]]; then
    sudo apt-get install -y libffi-dev
    sudo apt-get install -y graphviz
    sudo apt-get install -y git-lfs
    sudo apt-get install -y ccache
else
    brew install graphviz
    brew install git-lfs
fi
conda activate 37
pip install -U pip

if [[ $(uname) = "Darwin" ]]; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew update && brew upgrade
    brew install openssl
fi

$DIR/upgrade.sh
