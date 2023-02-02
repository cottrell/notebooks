#!/bin/bash -e
if [[ $(uname) = "Linux" ]]; then
    echo installing for Ubuntu
    # Add the release PGP keys:
    sudo curl -o /usr/share/keyrings/syncthing-archive-keyring.gpg https://syncthing.net/release-key.gpg
    # Add the "stable" channel to your APT sources:
    echo "deb [signed-by=/usr/share/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list
    # Update and install syncthing:
    sudo apt-get update
    sudo apt-get install syncthing
elif [[ $(uname) = "Darwin" ]]; then
    # brew is a pain and slow but maybe stick with it
    echo installing for MacOS using brew
    brew upgrade syncthing
    # brew list syncthing && brew upgrade syncthing || brew install syncthing

    # or direct from download
    # url=https://github.com/syncthing/syncthing/releases/download/v1.12.0/syncthing-macos-amd64-v1.12.0.zip
    # base=$(basename $url)
    # if [[ ! -e $base ]]; then
    #     wget $url
    # fi
    # unzip $base
    # sudo cp -v $base/syncthing /usr/local/bin
    # echo cleanup manually when done ...
else
    echo unknown uname $(uname)
    exit 1
fi
