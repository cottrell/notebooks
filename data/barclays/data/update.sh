#!/bin/sh
for x in isa chequing saver; do
    b=$(ls -rt "$x"_2014*.csv | tail -1)
    target="$x"_present.csv
    if [ -e $b ]; then
        if [ -e $target ]; then
            dl $target
        fi
        ln -vs $b $target
    fi
done
