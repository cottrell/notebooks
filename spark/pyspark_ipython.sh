#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# remember derby is single instance only so you will get errors starting two of these in same pwd
PATH=$PATH:~/dev/spark-2.2.0-bin-hadoop2.7/bin
export SPARK_CONF_DIR=$DIR/conf
export PYSPARK_DRIVER_PYTHON=ipython
env
pyspark --verbose
