#!/bin/sh

if [ $# -ne 1 ]; then
    echo usage: prog to_remove
    exit 1
fi

echo '# echoing commands, review and run, they are probably redundant'
echo sudo apt-get remove $1
echo sudo apt-get autoremove $1
echo sudo apt-get purge $1
echo sudo apt-get autoremove --purge $1
