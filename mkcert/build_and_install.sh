#!/bin/bash -e
cd ${HOME}/dev
[ -e mkcert ] || git clone https://github.com/FiloSottile/mkcert
cd mkcert
go build -ldflags "-X main.Version=$(git describe --tags)"
sudo cp -v mkcert /usr/local/bin
type mkcert
