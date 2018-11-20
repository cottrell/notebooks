#!/bin/sh
xidel http://spark.apache.org/ -e '//a[@href="/docs/latest/"]/text()' | sed -n "s/Latest Release (Spark \(.*\))/\1/p" > version.txt
