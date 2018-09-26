#!/bin/sh
# SOURCE THIS OR RUN IT!
ENVDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SPARK_HOME=~/dev/spark-2.3.2-bin-hadoop2.7
PATH=$PATH:$SPARK_HOME/bin
PYTHONPATH=$PYTHONPATH:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.6-src.zip
PYTHONPATH=$ENVDIR:$PYTHONPATH

# NOTES: for local you want executor memory to be near max likely

case $1 in
    pyspark_ipython)
        export PYSPARK_DRIVER_PYTHON=ipython
        # I HAVE NO IDEA ABOUT THIS SETTINGS IN STANDALONE MODE
        # --conf spark.sql.shuffle.partitions=8 \
        pyspark \
            --conf spark.sql.execution.arrow.enabled=true \
            --conf spark.driver.memory='16g' \
            --conf spark.executor.memory='8g' \
            --conf spark.sql.shuffle.partitions=1
        ;;
    spark-submit)
        # TODO test
        shift
        spark-submit \
            --conf spark.sql.execution.arrow.enabled=true \
            --conf spark.driver.memory='16g' \
            --conf spark.executor.memory='8g' \
            --conf spark.sql.shuffle.partitions=1 $*
        ;;
    *)
        ;;
esac
