#!/bin/sh
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

function kaggle_paginator() {
    # base=$(mktemp -d)
    base=$1
    mkdir -p $base
    fun=$2
    i=1
    more_pages=true
    while $more_pages; do
        filename=$base/$i
        if [ -e $filename ]; then
            echo found $filename >&2
        else
            echo getting $filename >&2
            $fun --page $i > $filename
        fi
        if grep -q '^No .* found' $filename; then
            echo "end of results reached at $i" >&2
            rm $filename
            head -1 $base/1
            for x in $base/*; do
                sed -e 1,1d $x
            done
            return
        fi
        i=$((i + 1))
    done
}

case $1 in
    datasets)
        kaggle_paginator /tmp/kaggle_datasets "kaggle d list --csv" > $DIR/kaggle_datasets.csv
        echo see $DIR/kaggle_datasets.csv
        ;;
    competitions)
        kaggle_paginator /tmp/kaggle_competitions "kaggle c list --csv" > $DIR/kaggle_competitions.csv
        echo see $DIR/kaggle_competitions.csv
        ;;
    *)
        echo dunno
esac
