#!/bin/bash -e
git pull &
git submodule foreach --recursive 'git checkout master; git pull origin master:master & :'
wait
