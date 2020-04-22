#!/bin/bash
if [[ "$#" -ne 1 ]]; then
    >&2 echo usage: $0 file
    exit 1
fi
cat $1 | (read -r; printf "%s\n" "$REPLY"; sort -t, -k3) | awk -F, '{ print $3 "," $1 "," $2}'
