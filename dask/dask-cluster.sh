#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case $1 in
    start)
        dask-scheduler &
        echo $! > $DIR/.dask-scheduler.pid
        dask-worker localhost:8786 &
        echo $! > $DIR/.dask-worker.pid
        ;;
    stop)
        kill $(cat $DIR/.dask-scheduler.pid)
        kill $(cat $DIR/.dask-worker.pid)
        ;;
    *)
        echo 'usage: prod start|stop'
        ;;
esac
