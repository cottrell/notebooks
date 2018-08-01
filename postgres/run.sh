#!/bin/sh
export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

dbdir=/var/tmp/postgres_test_db
logfile=$DIR/pg.log

mkdir -p $dbdir

case $1 in
    init)
        pg_ctl -D /var/tmp/postgres_test_db -l $logfile initdb
        ;;
    start)
        pg_ctl -D /var/tmp/postgres_test_db -l $logfile start
        ;;
    stop)
        pg_ctl -D /var/tmp/postgres_test_db stop
        ;;
    *)
        echo dunno
        exit 1
        ;;
esac
