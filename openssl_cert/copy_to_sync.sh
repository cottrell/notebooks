#!/bin/bash
sync=$HOME/syncthing/cred/openssl_cert/$(hostname)
mkdir -p $sync
mv -v rootCA.{srl,key,pem} device.key $(hostname).{crt,csr} $sync
