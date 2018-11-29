#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

function maybe_get {
    base=$(basename $1)
    if [[ -e "$base" ]]; then
        echo $base exists
    else
        wget $1
    fi
}

version=$(head -1 $DIR/version.txt)
echo version=$version
sleep 1

maybe_get  http://www.apache.org/dist/spark/spark-$version/spark-"$version"-bin-hadoop2.7.tgz
maybe_get https://www.apache.org/dist/spark/KEYS
maybe_get  http://www.apache.org/dist/spark/spark-"$version"/spark-"$version"-bin-hadoop2.7.tgz.asc
# maybe_get  http://www.apache.org/dist/spark/spark-"$version"/spark-"$version"-bin-hadoop2.7.tgz.md5
maybe_get  http://www.apache.org/dist/spark/spark-"$version"/spark-"$version"-bin-hadoop2.7.tgz.sha512

# md5_file=$(md5 spark-"$version"-bin-hadoop2.7.tgz | cut -d= -f2 | sed -e 's/ //' | tr '[:upper:]' '[:lower:]')
# md5_orig=$(cat spark-"$version"-bin-hadoop2.7.tgz.md5 | cut -d: -f2 | sed -e 's/ //g' | tr '[:upper:]' '[:lower:]')
sha_file=$(shasum -a 512 spark-"$version"-bin-hadoop2.7.tgz | cut -d' ' -f1 )
sha_orig=$(cat spark-"$version"-bin-hadoop2.7.tgz.sha512 | cut -d: -f2 | sed -e 's/ //g' | tr '[:upper:]' '[:lower:]' | paste -s -d'\0' -)
if [[ "$sha_file" = "$sha_orig" ]]; then
    echo "sha pass"
else
    echo "sha fail <$sha_file> vs <$sha_orig>"
fi

gpg --import KEYS
gpg --verify spark-"$version"-bin-hadoop2.7.tgz.asc spark-"$version"-bin-hadoop2.7.tgz && echo '.asc pass' || echo '.asc fail'

if [[ -d "$HOME/dev/spark-$version-bin-hadoop2.7" ]]; then
    echo ~/dev/spark-$version-bin-hadoop2.7 exists
else
    echo untarring to ~/dev
    tar -xzf ./spark-$version-bin-hadoop2.7.tgz -C ~/dev
fi
echo To clean up: rm -rf KEYS spark-$version-bin-hadoop2.7.tgz spark-$version-bin-hadoop2.7.tgz.asc spark-$version-bin-hadoop2.7.tgz.sha512 spark-$version-bin-hadoop2.7.tgz.sha512
echo "add this manually to .bash_aliases"
echo alias "pyspark_ipython='PYSPARK_DRIVER_PYTHON=ipython pyspark'"
echo "update your paths manually!"
echo SPARK_HOME=~/dev/spark-2.4.0-bin-hadoop2.7
echo PATH='$PATH:$SPARK_HOME/bin'
