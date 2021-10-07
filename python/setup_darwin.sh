#!/bin/bash -e
DIR="$( cd "$(dirname "$0")" ; pwd -P )"
type gcc || echo no gcc installed!

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew update && brew upgrade
brew install openssl

type wget || brew install wget
type graphviz || brew install graphviz
type git-lfs || brew install git-lfs
brew upgrade graphviz
brew upgrade git-lfs

