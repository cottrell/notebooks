# http://inoryy.com/post/tensorflow2-deep-reinforcement-learning/
# conda env remove --name tf2
conda create -n tf2gpu python=3.6
source activate tf2gpu
# pip install tf-nightly-2.0-preview ipython gym
# need to install nvidia 10 driver manually
pip install tf-nightly-gpu-2.0-preview ipython
