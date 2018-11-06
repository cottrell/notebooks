#!/bin/sh -e

# consider using miniconda
# https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

if [[ $(uname) -eq Linux ]]; then
    filename=Anaconda3-5.3.0-MacOSX-x86_64.sh
else
    filename=Anaconda3-5.3.0-Linux-x86_64.sh
fi
echo $filename

cd /tmp
if [[ -e $filename ]]; then
    echo $filename exists
else
    wget https://repo.anaconda.com/archive/$filename
fi

[ -e ~/anaconda3 ] || bash ./$filename -u

# continually rerunning this this will not necessarily lead to stable deployment state, just for human setup
# if you try 37 will just get downgraded by some packages as of 2018-11
if [ ! $(conda info --envs | grep 36) ]; then
    echo ~/anaconda3/bin/conda create -n 36 python=3.6 pandas
    ~/anaconda3/bin/conda create -y -n 36 python=3.6 pandas
else
    echo 36 exists
fi
source ~/anaconda3/bin/activate 36
echo installing packages
conda install -y pip pandas ipython scipy Cython scikit-learn tensorflow keras tensorboard setuptools ujson
conda install -y -c conda-forge xgboost nodejs
# if you have problems with node, clear the ~/.npm dir
# nodejs # maybe do not install node like this
# brew install node

conda install -y pytorch torchvision -c pytorch
pip install --upgrade pip
pip install GPy lightgbm catboost
