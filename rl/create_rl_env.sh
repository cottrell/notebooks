#!/bin/sh
# first install anaconda3
if [ ! $(conda info --envs | grep rl) ]; then
    echo ~/anaconda3/bin/conda create -n rl python=3.6
    conda create -y -n rl python=3.6
else
    echo rl exists
fi

pip install -r requirements.txt

# never finishes
# pip install pybullet==2.3.6
pip install pybullet

