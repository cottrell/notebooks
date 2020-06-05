#!/bin/bash
if [[ $(uname) = Darwin ]]; then
    cat ./environment.pip | sed -e 's/tensorflow-gpu/tensorflow/' > /tmp/environment.pip
    pip install -r /tmp/environment.pip -U
else
    pip install -r ./environment.pip -U
fi

jupyter labextension install @jupyterlab/vega3-extension

conda install -c conda-forge nodejs
