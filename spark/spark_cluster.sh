#!/bin/sh -e
# YOU MUST BOUNCE THE CLUSTER FOR ANY CHANGES TO TAKE EFFEcT
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh

case $1 in
    start)
        start-master.sh
        start-slave.sh $SPARK_MASTER_URL
        ;;
    stop)
        stop-master.sh
        stop-slave.sh $SPARK_MASTER_URL
        ;;
esac
