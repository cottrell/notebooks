#!/bin/sh

# because things are not importable as they are
# example: cp.sh code/Chapter02/*py

for x in $*; do
    a=$(basename $x | cut -d'_' -f1)
    b=$(basename $x | cut -d'_' -f2- | cut -d'.' -f1)
    filename="$b"_$a.py
    if [ -e $filename ]; then
        echo "$filename exists!"
    else
        cp -v $x $filename
    fi
done
