#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

whois_dir="$DIR/data/whois"
log_dir="$DIR/data/logs"
mkdir -p "$log_dir"
mkdir -p "$whois_dir"
echo ip,date > timeseries.csv
grep DoS $log_dir/20*.log | sort -u | sed  's/^.*from source: \([^:]*\)[^ ]* \(.*\)$/\1\|\2/' | sed 's/,/ /g;s/  / /g;s/|/,/g;s/\s*$//' >> $DIR/data/timeseries.csv

for x in $(grep DoS $log_dir/20*.log | sort -u | sed  's/^.*from source: \([^:]*\)[^ ]* \(.*\)$/\1/'); do
    if [[ ! -e $whois_dir/$x ]]; then
        echo whois $x
        whois $x > $whois_dir/$x
    fi
done

grep Organization $whois_dir/* | cut -d: -f3 | sed -e 's/ *//' | sort | uniq -c | sort -g
