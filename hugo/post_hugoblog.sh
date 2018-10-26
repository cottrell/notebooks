#!/bin/sh -e
# run this FROM the hugo dir!
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ "$1" ]]; then
    $DIR/do.sh post $1
    cd $DIR/hugoblog
    git add content/notes/$1.md
    git status
    cd -
else
    cd $DIR/hugoblog/content/notes
    vi .
    cd -
fi
