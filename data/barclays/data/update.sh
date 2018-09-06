#!/bin/sh
dl *_present.csv > /dev/null 2>&1
for x in isa chequing saver; do
    b=$(ls -rt "$x"_*.csv | tail -1)
    ln -vs $b "$x"_present.csv
done
