#!/bin/sh -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/hugoblog
hugo
mkdir -p ../../docs
cp -vR public/* ../../docs
cmd="cd $DIR/.. && ls && git add ./docs && git commit -m 'update docs' && git push"
echo
read -p "RUN command $cmd ? " -n 1 -r </dev/tty
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo got yes
    eval $cmd
else
    echo
    echo not committing and pushing
fi
