#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

[[ -d $DIR/whois ]] || mkdir -p $DIR/whois

for x in $(grep DoS $DIR/20*.log | cut -d: -f6- | cut -d' ' -f2 | cut -d: -f1 | sort -u); do
    if [[ ! -e $DIR/whois/$x ]]; then
        echo whois $x
        whois $x > $DIR/whois/$x
    fi
done

grep Organization $DIR/whois/* | cut -d: -f3 | sed -e 's/ *//' | sort | uniq -c | sort -g
