#!/bin/sh
# run this FROM the hugo dir!
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ "$1" ]]; then
    cd $DIR/h
    $DIR/do.sh post $1
else
    vi $DIR/h/content/posts
fi
