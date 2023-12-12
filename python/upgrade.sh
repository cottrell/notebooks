#!/bin/bash
pip install --upgrade pip

# ENV_FILE=requirements.pip
ENV_FILE=requirements_minimal.pip

# if [[ $(uname) = Darwin ]]; then
if [[ $(hostname) != bleepblop ]]; then
    echo do not use GPU on this machine
    cat $ENV_FILE | sed -e 's/tensorflow-gpu/tensorflow/' > /tmp/requirements.pip
    echo jax >> /tmp/requirements.pip
    # pip install -r /tmp/requirements.pip -U  # some conflicts causing issues
    for x in $(cat /tmp/requirements.pip); do
        pip install -U $x
    done
else
    echo use GPU on this machine
    # pip install -r $ENV_FILE -U  # some conflicts causing issues
    for x in $(cat $ENV_FILE); do
        pip install -U $x
    done
    # 2023-10-23
    pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
    # pip install --upgrade "jax[cuda11_local]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
    # pip install --upgrade "jax[cuda12_local]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
    # pip install --upgrade jax[cuda12_pip] -f https://storage.googleapis.com/jax-releases/jax_releases.html
    # pip install --upgrade jax[cuda12_local] -f https://storage.googleapis.com/jax-releases/jax_releases.html  # some other alternative
    # pip install --upgrade jax[cuda111] -f https://storage.googleapis.com/jax-releases/jax_releases.html
    # pip install --upgrade "jax[cuda]" -f https://storage.googleapis.com/jax-releases/jax_releases.html  # Note: wheels only available on linux.

fi
# # for some reason this fails in upgrade mode as of 2020-06-04
# pip install cvxpy

# jupyter labextension install @jupyterlab/vega3-extension
# only required if you have not enabled the ipywidgets nbextension yet
# jupyter nbextension enable --py --sys-prefix widgetsnbextension

# maybe just rely on primary node, npm
# conda install -c conda-forge nodejs

# see https://plotly.com/python/getting-started/ for plotly
# jupyter labextension install jupyterlab-plotly
# jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget
