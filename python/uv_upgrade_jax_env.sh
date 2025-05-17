#!/bin/bash -e
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

. $HOME/uv_venvs/uv_3.12_jax/bin/activate

uv pip install --upgrade pip

ENV_FILE=requirements_minimal.txt
cat $ENV_FILE > /tmp/requirements.pip

if [[ $(hostname) != bleepblop ]]; then
    echo do not use GPU on this machine
    echo jax >> /tmp/requirements.pip
else
    echo use GPU on this machine
    echo "jax[cuda12]" >> /tmp/requirements.pip
fi
uv pip install -r $ENV_FILE -U
