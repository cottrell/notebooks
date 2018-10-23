#!/bin/sh
for x in $(cat libs.txt); do
    b=$(basename $x)
    [[ -e $b ]] && echo exists: $b || wget $x
done
