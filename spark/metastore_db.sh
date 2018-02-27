#!/bin/sh -e
# brew install postgres
# https://www.cloudera.com/documentation/enterprise/5-6-x/topics/cm_ig_extrnl_pstgrs.html#cmig_topic_5_6

pg_isready && pg_ctl -D /var/tmp/postgres_metastore_db stop
METASTORE_DIR=/var/tmp/postgres_metastore_db
echo METASTORE_DIR=$METASTORE_DIR
rm -rf $METASTORE_DIR

initdb -D $METASTORE_DIR
if [[ $(grep 'host\s\+all\s\+all\s\+127.0.0.1/32\s\+ident' $METASTORE_DIR/pg_hba.conf) ]]; then
    echo check on ident in pg_hbd.conf you need to prob insert before this. do something with broken sed on osx
    exit
else
    echo 'host all all 127.0.0.1/32 md5' >> $METASTORE_DIR/pg_hba.conf
fi

echo "listen_addresses = '*'" >> $METASTORE_DIR/postgresql.conf
echo THIS IS postgressq.conf
cat $METASTORE_DIR/postgresql.conf | grep -v '^\s*[#]' | grep -v '^$'

# shared_buffers - 256MB
# wal_buffers - 8MB
# checkpoint_segments - 16
# checkpoint_completion_target - 0.9
# RHEL
# $ sudo /sbin/chkconfig postgresql on
# $ sudo /sbin/chkconfig --list postgresql
# $ service postgresql restart

pg_ctl -D /var/tmp/postgres_metastore_db -l $METASTORE_DIR/logfile start
cat $METASTORE_DIR/logfile

psql postgres <<STDIN
CREATE ROLE hive LOGIN PASSWORD 'hive_password';
CREATE DATABASE metastore OWNER hive ENCODING 'UTF8';
ALTER DATABASE metastore SET standard_conforming_strings = off;
STDIN

