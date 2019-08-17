#!/bin/sh

# wget https://github.com/emcrisostomo/fswatch/archive/1.11.3.tar.gz
if [[ $(uname -s) = 'Darwin' ]]; then
    brew install fswatch
fi
