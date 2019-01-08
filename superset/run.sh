#!/bin/bash -e

case $1 in
    install)
        conda create -n superset || :
        source activate superset
        sudo apt-get install libsasl2-dev
        pip install psycopg2
        pip install superset
        fabmanager create-admin --app superset
        source activate superset
        superset db upgrade
        superset load_examples
        superset init
        ;;
    run)
        source activate superset
        superset runserver -d -p 8088
        ;;
    *)
        echo 'run.sh install|run'
        ;;
esac

