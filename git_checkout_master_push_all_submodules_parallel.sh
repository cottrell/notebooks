#!/bin/bash -e
# git submodule foreach --recursive 'git checkout master && git push origin master & :'
git submodule foreach --recursive '
  branch=$(git rev-parse --verify master 2>/dev/null 1>&2 && echo master || echo main);
  git checkout $branch;
  git push origin $branch & :
'
# branch=$(git rev-parse --verify master 2>/dev/null 1>&2 && echo master || echo main);
# git push origin $branch
git push origin
wait
