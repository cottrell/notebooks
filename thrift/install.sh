#!/bin/sh -e

cd ~/dev
if [ ! -d thrift-0.11.0 ]; then
    wget http://apache.mirror.anlx.net/thrift/0.11.0/thrift-0.11.0.tar.gz
    tar -xvzf thrift-0.11.0.tar.gz
fi
cd thrift-0.11.0
ls
./bootstrap.sh
./configure
make
make check
sh test/test.sh
sudo make install
# copy/pasta waiting for complete ... probably didn't work if not hear back
