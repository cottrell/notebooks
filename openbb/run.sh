#!/bin/bash -e
. $HOME/anaconda3/etc/profile.d/conda.sh
conda activate obb
cd ~/dev/OpenBBTerminal
python terminal.py
