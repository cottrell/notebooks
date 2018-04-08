#!/bin/sh
trap "kill -- -$$" EXIT
exec "$@"
