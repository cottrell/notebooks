#!/bin/sh
# does not work, project seems too old too install first try
case $1 in
    init)
        conda create -n hugo_jupyter
        source activate jugo_jupyter
        pip install hugo_jupyter
        hugo_jupyter --init
        echo 'theme = "ananke"' >> config.toml
        ;;
    serve)
        fab serve
        ;;
    *)
        echo dunno
        exit 1
        ;;
esac
