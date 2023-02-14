#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo usage: prog username [since]
    exit 1
fi
since="${since:-2006-03-26}"
username=$(echo $1 | tr '[:upper:]' '[:lower:]')
filename=twint_"$username"_following.csv
cmd="twint --since $since --username $username --following --csv --output $filename"
# resume does not seem to work as expected, I think it goes backwards not forwards
# if [[ -f $filename ]]; then
#     # WARNING: fragile tab delimited file parsing relying on id being first entry in 2nd row
#     id=$(head -2 $filename | tail -1 | cut -d'	' -f1)
#     cmd="$cmd --resume $id"
# fi
echo $cmd
eval $cmd

