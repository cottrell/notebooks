#!/bin/sh

# because things are not importable as they are
# example: cp.sh code/Chapter02/*py

for x in */Chapter*; do
    c=$(basename $x | sed -e 's/Chapter//')
    if [ -e ch$c ]; then
        echo ch$c exists!
    else
        cp -v -R $x ch$c
        touch ch$c/__init__.py
    fi
done
