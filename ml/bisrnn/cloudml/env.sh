#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# export BUCKET="misc-data-ml" # gcloud
export BUCKET="misc-data-ml-cottrell" # S3

# export BUCKET="misc-data-ml-us"
export JOB_NAME="job_$(date +%Y%m%d_%H%M%S)"
export FILENAME=$DIR/../mangled_data.txt.gz
export GCS_FILENAME=gs://${BUCKET}/mangled_data.txt.gz
# export CLOUDSDK_PYTHON=
if [ "$(uname)" = "Darwin" ]; then
	echo I think I am OSX
	# gcloud is only python2.7 !!! horrible
	source ${HOME}/anaconda3/envs/36/bin/activate py27
else
	echo uname is $(uname)
fi
