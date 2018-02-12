#!/bin/sh
# remember derby is single instance only so you will get errors starting two of these in same pwd
PATH=$PATH:~/dev/spark-2.2.0-bin-hadoop2.7/bin
export PYSPARK_DRIVER_PYTHON=ipython
pyspark
