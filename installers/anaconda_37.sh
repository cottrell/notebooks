#!/bin/bash -e
#############
# MONSTER ENV
#############

# consider using miniconda
# https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

if [[ $(uname) = "Linux" ]]; then
    filename=Anaconda3-5.3.1-Linux-x86_64.sh
else
    filename=Anaconda3-5.3.1-MacOSX-x86_64.sh
fi
echo Will install: $filename

cd /tmp
if [[ -e $filename ]]; then
    echo $filename exists
else
    wget https://repo.anaconda.com/archive/$filename
fi

[[ -e ~/anaconda3 ]] || bash ./$filename -u

# continually rerunning this this will not necessarily lead to stable deployment state, just for human setup
# if you try 37 will just get downgraded by some packages as of 2018-11
if [[ ! $(conda info --envs | grep 37) ]]; then
    echo ~/anaconda3/bin/conda create -n 37 python=3.7 pandas
    ~/anaconda3/bin/conda create -y -n 37 python=3.7 pandas
else
    echo 37 exists
fi
source ~/anaconda3/bin/activate 36
echo installing packages
conda install -y pip pandas ipython scipy Cython jupyter setuptools ujson
conda install -y matplotlib seaborn bokeh
conda install -y -c conda-forge xgboost nodejs jupyterlab
conda install -y pytorch torchvision -c pytorch
# conda install -y pytorch-gpu torchvision -c pytorch

pip install --upgrade pip
# pip install --upgrade tensorboard tensorflow-probability
if [[ $(uname) = "Linux" ]]; then
	# pip install tensorflow-gpu
	# pip install tensorflow
	# pip install tf-nightly
	# pip install tf-nightly-gpu
        # conda install -c anaconda tensorflow-gpu
        echo skip tf

else
	# pip install tensorflow
        echo skip tf
fi
pip install scikit-learn auto-sklearn

# if you have problems with node, clear the ~/.npm dir

pip install lightgbm catboost

# not really but why not
# pip install dask argh pyarrow bcolz toolz cloudpickle pandas_datareader
pip install boto3

hub

cd ~/dev
hub clone EpistasisLab/tpot
cd tpot && python setup.py develop; cd -

cd ~/dev
hub clone jhfjhfj1/autokeras && cd autokeras && python setup.py develop; cd -

# NOTES, YOU PROBABLY DON't want to live run this without reading
source activate 36
# dev clones
cd ~/dev
sudo apt install swig
hub clone automl/auto-sklearn
cd ~/dev/tensorflow
[[ -e tensorflow ]] || hub clone tensorflow/tensorflow
[[ -e probability ]] || hub clone tensorflow/probability
[[ -e models ]] || hub clone tensorflow/models
