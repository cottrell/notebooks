#!/bin/bash
if [[ $(uname) = Darwin ]]; then
    cat ./environment.pip | sed -e 's/tensorflow-gpu/tensorflow/' > /tmp/environment.pip
    pip install -r /tmp/environment.pip -U
else
    pip install -r ./environment.pip -U
fi
# for some reason this fails in upgrade mode as of 2020-06-04
pip install cvxpy

jupyter labextension install @jupyterlab/vega3-extension

jupyter nbextension enable --py --sys-prefix qgrid
# only required if you have not enabled the ipywidgets nbextension yet
jupyter nbextension enable --py --sys-prefix widgetsnbextension

# maybe just rely on primary node, npm
# conda install -c conda-forge nodejs
