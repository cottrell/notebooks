#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# manually get the max N %% 20
case $1 in
    datasets)
        bbb=datasets
        base=kaggle_"$bbb"_
        rm /tmp/"$base"*.csv || :
        for i in $(seq 1 13); do
            kaggle $bbb list --page $i --csv > /tmp/"$base"$i.csv &
        done
        wait
        (
        head -1 /tmp/"$base"1.csv
        for x in /tmp/"$base"*.csv; do
            sed -e 1,1d $x
        done
        ) > $DIR/kaggle_datasets.csv
        ;;
    competitions)
        bbb=competitions
        base=kaggle_"$bbb"_
        rm /tmp/"$base"*.csv || :
        for i in $(seq 1 13); do
            kaggle $bbb list --page $i --csv > /tmp/"$base"$i.csv &
        done
        wait
        (
        head -1 /tmp/"$base"1.csv
        for x in /tmp/"$base"*.csv; do
            sed -e 1,1d $x
        done
        ) > $DIR/kaggle_competitions.csv
        ;;
    *)
        echo dunno
esac
