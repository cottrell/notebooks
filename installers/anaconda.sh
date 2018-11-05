#!/bin/sh -e

if [[ $(uname) -eq Linux ]]; then
    filename=Anaconda3-5.3.0-MacOSX-x86_64.sh
else
    filename=Anaconda3-5.3.0-Linux-x86_64.sh
fi
echo $filename

cd /tmp
if [[ -e $filename ]]; then
    echo $filename exists
else
    wget https://repo.anaconda.com/archive/$filename
fi

bash ./$filename -u

~/anaconda3/bin/conda create -n 37 pandas
