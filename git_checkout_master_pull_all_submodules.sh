#!/bin/bash -e
git pull # you forget this
# ugh
# master=$(git rev-parse --verify master 2>/dev/null 1>&2 && echo master || echo main)
# git submodule foreach --recursive 'git checkout master; git pull origin master:master; :'
git submodule foreach --recursive 'git checkout master; git pull origin master:master; :'
