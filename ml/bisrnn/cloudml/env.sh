#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export BUCKET="misc-data-ml"
export JOB_NAME="job_$(date +%Y%m%d_%H%M%S)"
export FILENAME=$DIR/../mangled_data.txt.gz
export GCS_FILENAME=gs://${BUCKET}/${FILENAME}
# gcloud is maybe only python2.7???
source ${HOME}/anaconda3/envs/36/bin/activate 36