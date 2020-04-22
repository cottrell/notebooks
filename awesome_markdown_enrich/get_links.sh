#!/bin/bash
if [[ "$#" -ne 1 ]]; then
    >&2 echo usage: $0 filename
    exit 1
fi
sed -e 's/.*\[\(.*\)\](\([^#][^)]*\)).*/\1,\2/;t;d' $1 | grep 'bitbucket\|github\|gitlab'

