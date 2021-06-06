#!/bin/bash -e
ORG=syncthing
REPO=syncthing

get_latest_version() {
    git -c 'versionsort.suffix=-' ls-remote --exit-code --refs --sort='version:refname' --tags https://github.com/$ORG/$REPO.git '*.*.*' | tail -1 | cut -d'/' -f3
}

version=$(get_latest_version)
url=https://github.com/$ORG/$REPO/releases/download/$version/syncthing-macos-amd64-$version.zip
echo Will install url=$url
base=$(basename $url)
if [[ ! -e $base ]]; then
    wget $url
fi
base_nozip=$(echo $base | sed -e 's/\.zip$//')
if [[ ! -e $base_nozip ]]; then
    unzip $base
fi
sudo cp -v $base_nozip/syncthing /usr/local/bin
echo WARNING: You must cleanup manually when done ...
