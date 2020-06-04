#!/bin/bash
pip install -r ./environment.pip -U
# for some reason this fails in upgrade mode as of 2020-06-04
pip install cvxpy

jupyter labextension install @jupyterlab/vega3-extension

jupyter nbextension enable --py --sys-prefix qgrid
# # only required if you have not enabled the ipywidgets nbextension yet
# jupyter nbextension enable --py --sys-prefix widgetsnbextension

conda install -c conda-forge nodejs
