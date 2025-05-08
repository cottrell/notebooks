#!/bin/bash -e
uv pip install --upgrade pip

ENV_FILE=requirements_minimal.txt

# if [[ $(uname) = Darwin ]]; then
if [[ $(hostname) != bleepblop ]]; then
    echo do not use GPU on this machine
    cat $ENV_FILE | sed -e 's/tensorflow-gpu/tensorflow/' > /tmp/requirements.pip
    echo jax >> /tmp/requirements.pip
    uv pip install -r /tmp/requirements.pip -U  # some conflicts causing issues
    # for x in $(cat /tmp/requirements.pip); do
    #     uv pip install -U $x
    # done
else
    echo use GPU on this machine
    uv pip install -r $ENV_FILE -U  # some conflicts causing issues
    # for x in $(cat $ENV_FILE); do
    #     uv pip install -U $x
    # done

    # 2024-10-01 ... jax and tensorflow can not be in same env at the moment.
    # 2024-08-22
    # uv pip install -U tensorflow[and-cuda]
    # 2024-07-10
    uv pip install -U "jax[cuda12]"
fi
