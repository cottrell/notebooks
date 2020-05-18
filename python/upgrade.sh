#!/bin/bash
pip install -r ./environment.pip -U

jupyter labextension install @jupyterlab/vega3-extension

conda install -c conda-forge nodejs
