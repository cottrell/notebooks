#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

[[ -d $DIR/whois ]] || mkdir -p $DIR/whois

echo ip,date > timeseries.csv
grep DoS $DIR/20*.log | sort -u | sed  's/^.*from source: \([^:]*\)[^ ]* \(.*\)$/\1\|\2/' | sed 's/,/ /g;s/  / /g;s/|/,/g;s/\s*$//' >> timeseries.csv

for x in $(grep DoS $DIR/20*.log | sort -u | sed  's/^.*from source: \([^:]*\)[^ ]* \(.*\)$/\1/'); do
    if [[ ! -e $DIR/whois/$x ]]; then
        echo whois $x
        whois $x > $DIR/whois/$x
    fi
done

grep Organization $DIR/whois/* | cut -d: -f3 | sed -e 's/ *//' | sort | uniq -c | sort -g
