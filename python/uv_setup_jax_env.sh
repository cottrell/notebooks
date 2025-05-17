#!/bin/bash -e
DIR="$( cd "$(dirname "$0")" ; pwd -P )"

type gcc 2>/dev/null || echo no gcc installed!
type uv 2>/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh

# WARNING: maybe you need to rebash after uv install

cd $HOME/uv_venvs

UV_ENV="uv_3.12_jax"
uv venv $UV_ENV --python 3.12
source $UV_ENV/bin/activate

$DIR/uv_upgrade_jax_env.sh
$DIR/uv_local_setup.sh
