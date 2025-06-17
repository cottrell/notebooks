#!/bin/bash

function list_cleanable() {
find . \
-type f -name "*.swp" -o \
-type f -name "*.pyc" -o \
-type d -name "__pycache__" -o \
-type d -name "node_modules" -o \
# -type d -name "build" -o \
-type d -name ".ipynb_checkpoints" -o \
-type d -name "*.egg-info" -o \
# -type d -name "joblib_cache*"
}

if [[ "$1" = yes ]]; then
    files=$(list_cleanable)
    for f in $files; do echo $f; done
    echo
    echo WILL MOVE THESE FILES TO .Trash!
    echo
    read -p "Are you sure (y for yes)? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo MOVING TO TRASH!
        echo before: $(du -sh)
        echo dl $files
        dl $files
        echo after: $(du -sh)
    fi
else
    list_cleanable
fi
