#!/bin/bash
export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
# 5432

dbdir=/var/tmp/postgres_test_db
# TODO docker this or whatever
# 1. manually set listen_addresses = '*' in postgressql.conf
# 2. manuallly pg_hba.conf host all all 0.0.0.0/0 md5
# 3. psql, then \password and manually set password
logfile=$DIR/pg.log

# \du
# \l
# sudo -u postgres psql postgres

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
