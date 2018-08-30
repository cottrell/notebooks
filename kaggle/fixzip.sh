#!/bin/sh

for x in *.zip; do
    b=$(echo $x | sed -e 's/\.zip//')
    echo "mkdir $b && mv $x $b"
done
