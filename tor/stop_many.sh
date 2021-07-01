#!/bin/bash -e
for x in $(ls pid.*); do
    pid=$(cat $x)
    sudo kill $pid && rm -v $x || :
done
