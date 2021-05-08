#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo usage: prog username [since]
    exit 1
fi
# since="${since:-2006-03-26}"
since="${since:-2016-01-21}"
username=$(echo $1 | tr '[:upper:]' '[:lower:]')
filename=twint_since_"$since"_$username.csv
cmd="twint --since $since --username $username --csv --output $filename"
# resume does not seem to work as expected, I think it goes backwards not forwards
# if [[ -f $filename ]]; then
#     # WARNING: fragile tab delimited file parsing relying on id being first entry in 2nd row
#     id=$(head -2 $filename | tail -1 | cut -d'	' -f1)
#     cmd="$cmd --resume $id"
# fi
echo $cmd
eval $cmd

