#!/bin/sh

FLASK_APP=example.py
if [[ "$1" ]]; then
    FLASK_APP=$1
fi
export FLASK_APP
flask run --host=0.0.0.0 --reload --debugger

