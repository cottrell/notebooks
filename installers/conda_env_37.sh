#!/bin/bash -e
#############
# MONSTER ENV
#############

source ./etc/profile.d/conda.sh
conda activate 37

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

pip install dask argh pyarrow bcolz toolz cloudpickle pandas_datareader
pip install boto3

hub

cd ~/dev
hub clone EpistasisLab/tpot
cd tpot && python setup.py develop; cd -

cd ~/dev
hub clone jhfjhfj1/autokeras && cd autokeras && python setup.py develop; cd -
