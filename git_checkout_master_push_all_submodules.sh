#!/bin/bash -e
# git submodule foreach --recursive 'git checkout master; git push origin master; :'

# plow through
# git submodule foreach --recursive 'git checkout master && git push origin master & :'

# debug, stop at first failure
git submodule foreach --recursive 'git checkout master && git push origin master'

git push origin master
