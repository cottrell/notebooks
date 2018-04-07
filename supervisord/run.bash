#!/bin/bash
trap "kill -- -$$" EXIT
export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
export ARXIVSANITYPATH=~/dev/arxiv-sanity-preserver
supervisord -c $DIR/supervisord.conf
tail -f /tmp/supervisord.log
echo 'then run supervisorctl'
