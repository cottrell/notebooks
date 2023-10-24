#!/bin/bash -e
git pull # you forget this
# git submodule foreach --recursive 'git checkout master; git pull origin master:master; :'
git submodule foreach --recursive '
  branch=$(git rev-parse --verify master 2>/dev/null 1>&2 && echo master || echo main);
  git checkout $branch;
  git pull origin $branch:$branch;
'
