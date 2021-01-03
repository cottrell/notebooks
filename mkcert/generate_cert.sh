#!/bin/bash -e
type certutil || sudo apt install libnss3-tools
localhostname=${1:-$(hostname)}
echo mkcert localhost $localhostname.local 127.0.0.1 ::1 # Generate the certs
mkcert $localhostname localhost 127.0.0.1 ::1 # Generate the certs
syncthing=$HOME/syncthing/cred/mkcert/$(hostname)
mkdir -p $syncthing
mv -v *pem $syncthing
echo "run this on server and on hosts to install:"
echo mkcert -install
