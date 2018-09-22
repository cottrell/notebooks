#!/bin/sh -e
# run this FROM the hugo dir!
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ "$1" ]]; then
    cd $DIR/hugoblog
    $DIR/do.sh post $1
else
    vi $DIR/hugoblog/content/posts
fi
