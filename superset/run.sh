#!/bin/sh

case $1 in
    install)
        # conda create -n superset
        source activate superset
        pip install superset
        fabmanager create-admin --app superset
        superset db upgrade
        superset load_examples
        superset init
        ;;
    run)
        superset runserver -d -p 8088
        ;;
    *)
        echo dunno
        ;;
esac

