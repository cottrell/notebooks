#!/bin/sh

# remember derby is single instance only so you will get errors starting two of these in same pwd

PATH=$PATH:/Users/davidcottrell/dev/spark-2.2.0-bin-hadoop2.7/bin
alias pyspark_ipython="PYSPARK_DRIVER_PYTHON=ipython pyspark"
pyspark
