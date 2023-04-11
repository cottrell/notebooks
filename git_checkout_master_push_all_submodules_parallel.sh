#!/bin/bash -e
git submodule foreach --recursive 'git checkout master && git push origin master & :'
git push origin master
wait
