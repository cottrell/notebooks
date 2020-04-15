#!/bin/bash
# https://github.com/Mottl/GetOldTweets3
if [[ $# -ne 1 ]]; then
    echo usage: prog username
fi
GetOldTweets3 --username $1 --since 2020-01-01 --emoji unicode --output get_old_$1.csv

