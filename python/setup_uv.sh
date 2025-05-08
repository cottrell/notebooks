#!/bin/bash -e
DIR="$( cd "$(dirname "$0")" ; pwd -P )"
# type gcc || echo no gcc installed!
type uv 2>/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh

# TODO: ongoing ... not really used yet
MY_UV_ENV=3.12
uv python install $MY_UV_ENV
uv venv $MY_UV_ENV
source $MY_UV_ENV/bin/activate

# THEN
# uv_upgrade.sh
# uv_local_setup.sh
