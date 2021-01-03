#!/bin/bash
base=https://dist.ipfs.io/go-ipfs
vfile=$base/versions
curl $vfile | tail -1 > version.txt
git diff version.txt
