#!/bin/bash -e

# https://repo.anaconda.com/archive/Anaconda3-2019.07-MacOSX-x86_64.sh
if [[ $(uname) = "Linux" ]]; then
    OS=Linux
else
    OS=MacOSX
fi
filename=Anaconda3-2019.07-$OS-x86_64.sh
echo Will install: $filename

cd /tmp
if [[ -e $filename ]]; then
    echo $filename exists
else
    wget https://repo.anaconda.com/archive/$filename
fi

[[ -e ~/anaconda3 ]] || bash ./$filename -u
