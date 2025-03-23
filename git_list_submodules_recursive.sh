#!/bin/bash
ROOT_DIR=$(pwd)
git submodule foreach --quiet --recursive 'echo "$(realpath --relative-to="'$ROOT_DIR'" "$(pwd)")"'
