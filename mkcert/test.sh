#!/bin/bash
type http-server || npm i -g http-server
base=$HOME/syncthing/cred/mkcert/$(hostname)/$(hostname)+3
echo http-server -S -C $base.pem -K $base-key.pem
http-server -S -C $base.pem -K $base-key.pem
