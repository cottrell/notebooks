#!/bin/bash -e
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

. $HOME/uv_venvs/uv_3.12_tf/bin/activate

uv pip install --upgrade pip

ENV_FILE=requirements_tf.txt
cat $ENV_FILE | grep -v tensorflow > /tmp/requirements_tf.pip

if [[ $(hostname) != bleepblop ]]; then
    echo do not use GPU on this machine
    echo tensorflow >> /tmp/requirements_tf.pip
    # for x in $(cat /tmp/requirements.pip); do
    #     uv pip install -U $x
    # done
else
    echo use GPU on this machine
    echo "tensorflow[and-cuda]" >> /tmp/requirements_tf.pip
fi

uv pip install -r /tmp/requirements_tf.pip -U
