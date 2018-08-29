#!/bin/sh

case $1 in
    datasets)
        rm /tmp/kaggle_*.csv
        for i in $(seq 1 13); do
            kaggle datasets list --page $i --csv > /tmp/kaggle_$i.csv &
        done
        wait
        cat /tmp/kaggle_*.csv
        ;;
    *)
        echo dunno
esac
