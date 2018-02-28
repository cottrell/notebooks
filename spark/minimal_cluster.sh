#!/bin/sh -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh

case $1 in
    start)
        start-master.sh
        start-slave.sh localhost:7077
        ;;
    stop)
        stop-master.sh
        stop-slave.sh localhost:7077
        ;;
esac
