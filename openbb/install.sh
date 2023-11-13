#!/bin/bash -e
. $HOME/anaconda3/etc/profile.d/conda.sh
cd ~/dev/OpenBBTerminal
conda env create -n obb --file build/conda/conda-3-10-env.yaml
conda activate obb
poetry install -E all
# conda install -c conda-forge tensorflow
# pip install -r requirements.txt
