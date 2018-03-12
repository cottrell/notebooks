#!/bin/sh -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh

# seems to work
[[ -e $DIR/postgresql-42.2.1.jre7.jar ]] || wget https://jdbc.postgresql.org/download/postgresql-42.2.1.jre7.jar
spark-submit --verbose \
    --jars $DIR/postgresql-42.2.1.jre7.jar \
    --master $SPARK_MASTER_URL \
    $@
