#!/bin/bash
# base=https://dist.ipfs.io/go-ipfs
base=https://dist.ipfs.tech/kubo
vfile=$base/versions
curl $vfile | tail -1 > version.txt
git diff version.txt
