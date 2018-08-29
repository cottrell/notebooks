#!/bin/sh
dl *_preset.csv
for x in isa chequing saver; do
    b=$(ls -rt "$x"_*.csv | tail -1)
    ln -vs $b "$x"_present.csv
done
