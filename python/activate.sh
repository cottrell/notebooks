#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
type deactivate 2>/dev/null && deactivate
. $DIR/uv_3.12_jax/bin/activate
