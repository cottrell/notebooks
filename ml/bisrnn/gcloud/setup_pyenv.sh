#!/bin/sh
conda create -n py27 python=2.7
source activate py27
pip install -r ./requirements.txt
