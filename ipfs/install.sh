#!/bin/bash
# REMINDER: do not use snap or brew ... too stale.

base=https://dist.ipfs.io/go-ipfs
vfile=$base/versions
curl $vfile | tail -1 > version.txt
version=$(cat version.txt)

if [[ $(uname) = "Darwin" ]]; then
    platform=darwin
elif [[ $(uname) = "Linux" ]]; then
    platform=linux
else
    echo bad platform $(uname)
    exit 1
fi

echo Will run with version $version platform $platform

filename=https://dist.ipfs.io/go-ipfs/$version/go-ipfs_"$version"_"$platform"-amd64.tar.gz
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
