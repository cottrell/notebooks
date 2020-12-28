#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo usage: prog username
    exit 1
fi
# since="${since:-2020-01-01}"
echo twint --username $1 --csv --output twint_$1.csv
twint --username $1 --csv --output twint_$1.csv

