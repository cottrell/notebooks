#!/bin/sh
export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

case $1 in
    start)
        pg_ctl -D /var/tmp/postgres_test_db -l /var/log/postgres_test_db.log start
        ;;
    stop)
        pg_ctl -D /var/tmp/postgres_test_db stop
        ;;
    *)
        echo dunno
        exit 1
        ;;
esac
