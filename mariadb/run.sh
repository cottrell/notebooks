#!/bin/sh

# see /usr/local/etc/my.cnf
# mysqld --verbose --options
# default port 3306

# mysql
# use information_schema;
# show tables;
# etc

case $1 in
    start)
        mysql.server start
        # --datadir=~/projects/db --user=mysql
        ;;
    stop)
        mysql.server stop
        # --datadir=~/projects/db --user=mysql
        ;;
    *)
        echo unknown arg $1
        exit 1
        ;;
esac
