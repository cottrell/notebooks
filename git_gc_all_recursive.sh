#!/bin/bash -e
git gc --aggressive --prune=now
git submodule foreach --recursive 'git gc --aggressive --prune=now'
