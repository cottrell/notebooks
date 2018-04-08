#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $DIR/env.sh
cd
jupyter lab --NotebookApp.iopub_data_rate_limit=10000000
