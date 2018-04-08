#!/bin/sh

PYSPARK_DRIVER_PYTHON=ipython
pyspark \
    --conf spark.sql.shuffle.partitions=8 \
    --conf spark.sql.execution.arrow.enabled=true
