#!/bin/bash
if [[ ! $# -eq 1 ]]; then
    echo usage: $0 host
    exit 1
fi
ssh -v -N -f -L 8300:localhost:8384 $1
