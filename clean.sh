#!/bin/bash

function list_cleanable() {
find . -type d \
-name "__pycache__" -o \
-name "node_modules" -o \
-name "build" -o \
-name ".ipynb_checkpoints" -o \
-name "joblib_cache*"
}

echo $1
if [[ "$1" = yes ]]; then
    list_cleanable > /dev/null
else
    list_cleanable
fi
