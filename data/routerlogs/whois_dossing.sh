#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

[[ -d $DIR/whois ]] || mkdir -p $DIR/whois

echo ip,date > timeseries.csv
grep DoS $DIR/20*.log | sort -u | cut -d: -f6- | sed -e 's/^ *//;s/ *$//' | sed -e 's/ /,"/;s/$/"/' >> timeseries.csv

for x in $(grep DoS $DIR/20*.log | sort -u | cut -d: -f6- | cut -d' ' -f2 | cut -d: -f1 | sort -u); do
    if [[ ! -e $DIR/whois/$x ]]; then
        echo whois $x
        whois $x > $DIR/whois/$x
    fi
done

grep Organization $DIR/whois/* | cut -d: -f3 | sed -e 's/ *//' | sort | uniq -c | sort -g

echo 'ip,key,value' > data.csv
cd $DIR/whois && grep '^[^%#]' * | grep -v '^$' | sed -E 's/: {1,}/,"/g;s/$/"/' | sed -e 's/:/,/' >> ../data.csv
cd -
