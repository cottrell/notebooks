#!/bin/bash
DIR=$HOME/uv_venvs
type deactivate 2>/dev/null && deactivate
. $DIR/uv_3.12_jax/bin/activate
