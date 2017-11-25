#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export BUCKET="misc-data-ml-cottrell" # S3
export LOCAL_FILENAME=$DIR/../mangled_data.txt.gz
export S3_FILENAME=s3://${BUCKET}/mangled_data.txt.gz
export JOB_NAME="job_$(date +%Y%m%d_%H%M%S)"
