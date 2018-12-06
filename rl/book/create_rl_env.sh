#!/bin/bash -e
# first install anaconda3
if [[ ! $(conda info --envs | grep rl) ]]; then
    echo ~/anaconda3/bin/conda create -n rl python=3.6
    conda create -y -n rl python=3.6
else
    echo rl exists
fi

# conda activate rl
source activate rl

conda install ipython

conda install tensorflow-gpu tensorboard
pip install -r requirements_mod.txt

[[ -d ~/dev/gym ]] || cd ~/dev && git clone https://github.com/openai/gym.git
cd ~/dev/gym && python setup.py develop

# conda install -y pytorch torchvision -c pytorch
# pip install atari-py ptan opencv-python tensorboardX tensorflow tensorboard
# pip install --upgrade pip


# never finishes
# pip install pybullet==2.3.6
pip install pybullet
