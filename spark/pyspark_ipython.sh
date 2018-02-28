#!/bin/sh -e
# maybe
# https://mail-archives.apache.org/mod_mbox/spark-user/201706.mbox/%3CMAXPR01MB0073181E0FBE16270733A762E4D30@MAXPR01MB0073.INDPRD01.PROD.OUTLOOK.COM%3E
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# remember derby is single instance only so you will get errors starting two of these in same pwd
PATH=$PATH:~/dev/spark-2.2.0-bin-hadoop2.7/bin
export SPARK_CONF_DIR=$DIR/conf
export HIVE_CONF_DIR=$SPARK_CONF_DIR
export PYSPARK_DRIVER_PYTHON=ipython
env
# # works
# pyspark --verbose --packages  org.postgresql:postgresql:42.2.1.jre7 --master spark://MacBook-Pro-3.local:7077

# does not work
# pyspark --verbose --packages  org.postgresql:postgresql:42.2.1.jre7 --master spark://localhost:7077

# seems to work
[[ -e $DIR/postgresql-42.2.1.jre7.jar ]] || wget https://jdbc.postgresql.org/download/postgresql-42.2.1.jre7.jar
pyspark --verbose --jars $DIR/postgresql-42.2.1.jre7.jar --master spark://MacBook-Pro-3.local:7077
