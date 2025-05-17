#!/bin/bash -e
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

. $HOME/uv_venvs/uv_3.12_pytorch/bin/activate

uv pip install --upgrade pip

ENV_FILE=requirements_pytorch.txt

# NOTE: no variation for GPU or CPU

uv pip install -r $ENV_FILE
