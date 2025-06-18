#!/bin/bash

git submodule foreach --recursive 'git remote get-url origin' | awk '/^Entering/ {sub(/^Entering '\''/, "", $0); sub(/'\''$/, "", $0); path=$0; next} {print path "\t" $0}'
