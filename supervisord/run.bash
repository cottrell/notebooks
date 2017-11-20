#!/bin/bash
trap "kill -- -$$" EXIT
export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
echo running supervisord -c $DIR/supervisord.conf
supervisord -c $DIR/supervisord.conf
echo 'then run supervisorctl'
# start thegroup:*
