#!/bin/bash
pip install --upgrade pip

# ENV_FILE=environment.pip
ENV_FILE=environment_minimal.pip

if [[ $(uname) = Darwin ]]; then
    # don't use GPU on Darwin
    cat $ENV_FILE | sed -e 's/tensorflow-gpu/tensorflow/' > /tmp/environment.pip
    echo jax >> /tmp/environment.pip
    # pip install -r /tmp/environment.pip -U  # some conflicts causing issues
    for x in $(cat /tmp/environment.pip); do
        pip install -U $x
    done
else
    # pip install -r $ENV_FILE -U  # some conflicts causing issues
    for x in $(cat $ENV_FILE); do
        pip install -U $x
    done
    pip install --upgrade jax[cuda111] -f https://storage.googleapis.com/jax-releases/jax_releases.html
fi
# # for some reason this fails in upgrade mode as of 2020-06-04
# pip install cvxpy

jupyter labextension install @jupyterlab/vega3-extension

jupyter nbextension enable --py --sys-prefix qgrid
# only required if you have not enabled the ipywidgets nbextension yet
jupyter nbextension enable --py --sys-prefix widgetsnbextension

# maybe just rely on primary node, npm
# conda install -c conda-forge nodejs

# see https://plotly.com/python/getting-started/ for plotly
jupyter labextension install jupyterlab-plotly
jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget
