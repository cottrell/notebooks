#!/bin/sh
PATH=$PATH:/Users/davidcottrell/dev/spark-2.3.0-bin-hadoop2.7/bin
PATH=$PATH:/Users/davidcottrell/dev/spark-2.3.0-bin-hadoop2.7/sbin
alias pyspark_ipython="PYSPARK_DRIVER_PYTHON=ipython pyspark"
export SPARK_CONF_DIR=$DIR/conf
export HIVE_CONF_DIR=$SPARK_CONF_DIR
export PYSPARK_DRIVER_PYTHON=ipython
export SPARK_MASTER_URL=spark://MacBook-Pro-3.local:7077
