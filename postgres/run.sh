#!/bin/sh
export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
# 5432

dbdir=/var/tmp/postgres_test_db
logfile=$DIR/pg.log

mkdir -p $dbdir

case $1 in
    init)
        pg_ctl -D $dbdir -l $logfile initdb
        ;;
    start)
        pg_ctl -D $dbdir -l $logfile start
        ;;
    connect)
        psql postgres
        ;;
    stop)
        pg_ctl -D $dbdir stop
        ;;
    *)
        echo dunno
        exit 1
        ;;
esac
