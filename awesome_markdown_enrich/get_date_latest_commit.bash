#!/bin/bash -e
if [[ "$#" -ne 1 ]]; then
    >&2 echo usage: $0 url
    exit 1
fi
tmp=$(mktemp -d)
cd $tmp
git clone -b master --single-branch $1 --depth=3 repo
cd repo
git log -1 --format="%at" | xargs -I{} date -d @{} +%Y-%m-%dT%H:%M:%S
cd ..
rm -rf repo
