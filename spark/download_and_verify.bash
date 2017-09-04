#!/bin/bash

function maybe_get {
    base=$(basename $1)
    [[ -e "$base" ]] || wget $1
}

version=2.2.0

maybe_get http://d3kbcqa49mib13.cloudfront.net/spark-"$version"-bin-hadoop2.7.tgz
maybe_get https://www.apache.org/dist/spark/KEYS
maybe_get http://www.apache.org/dist/spark/spark-"$version"/spark-"$version"-bin-hadoop2.7.tgz.asc
maybe_get http://www.apache.org/dist/spark/spark-"$version"/spark-"$version"-bin-hadoop2.7.tgz.md5
maybe_get http://www.apache.org/dist/spark/spark-"$version"/spark-"$version"-bin-hadoop2.7.tgz.sha

md5_file=$(md5 spark-"$version"-bin-hadoop2.7.tgz | cut -d= -f2 | sed -e 's/ //' | tr '[:upper:]' '[:lower:]')
md5_orig=$(cat spark-"$version"-bin-hadoop2.7.tgz.md5 | cut -d: -f2 | sed -e 's/ //g' | tr '[:upper:]' '[:lower:]')
if [[ "$md5_file" = "$md5_orig" ]]; then
    echo "md5 pass"
else
    echo "md5 fail <$md5_file> vs <$md5_orig>"
fi

gpg --import KEYS
gpg --verify spark-"$version"-bin-hadoop2.7.tgz.asc spark-"$version"-bin-hadoop2.7.tgz && echo '.asc pass' || echo '.asc fail'

echo untar and add spark-"$version"-bin-hadoop2.7/bin to PATH
echo alias pyspark_ipython='PYSPARK_DRIVER_PYTHON=ipython pyspark'
