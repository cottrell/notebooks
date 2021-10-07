#!/bin/bash -e
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

type gcc || echo no gcc installed!

sudo apt-get install -y libffi-dev
sudo apt-get install -y graphviz
sudo apt-get install -y git-lfs
sudo apt-get install -y ccache
