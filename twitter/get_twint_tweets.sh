#!/bin/bash -e
# I think twitter started in 2006-03-26
if [[ $# -lt 1 ]]; then
    echo usage: prog username [since]
    exit 1
fi
username=$1
shift
since=$1
since="${since:-2016-01-21}"
username=$(echo $username | tr '[:upper:]' '[:lower:]')
filename=twint_since_"$since"_$username.csv
cmd="twint --since $since --username $username --csv --output $filename"
echo $cmd
eval $cmd
gzip $filename
