#!/bin/bash

base=https://dist.ipfs.io/go-ipfs
vfile=$base/versions
curl $vfile | tail -1 > version.txt
version=$(cat version.txt)
echo Will run with version $version

filename=https://dist.ipfs.io/go-ipfs/$version/go-ipfs_"$version"_linux-amd64.tar.gz
localfile=$(basename $filename)
if [[ -e $localfile ]]; then
    echo $localfile found will not download again
else
    echo $localfile not found will not download again
    wget -v $filename
fi

if [[ ! -e $localfile ]]; then
    echo $localfile still not found
    exit 1
fi

tar -xvzf $localfile
cd go-ipfs
sudo bash install.sh

ipfs --version

echo Remember to delete tar file.
echo dl $localfile
echo dl go-ipfs