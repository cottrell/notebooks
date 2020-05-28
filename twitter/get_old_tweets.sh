#!/bin/bash
# https://github.com/Mottl/GetOldTweets3
if [[ $# -lt 1 ]]; then
    echo usage: prog username [since]
    exit 1
fi
since=$2
since="${since:-2020-01-01}"
GetOldTweets3 --username $1 --since $since --emoji unicode --output get_old_$1.csv

