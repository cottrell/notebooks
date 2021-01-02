#!/bin/bash -e
type certutil || sudo apt install libnss3-tools
localhostname=${1:-$(hostname)}
echo mkcert localhost $localhostname.local 127.0.0.1 ::1 # Generate the certs
mkcert localhost $localhostname.local 127.0.0.1 ::1 # Generate the certs
echo run this to install:
echo mkcert -install
