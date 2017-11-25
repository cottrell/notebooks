#!/bin/sh
DIR="$( cd "$(dirname "$0")" ; pwd -P )"
. ${DIR}/env.sh
echo aws s3 ls $S3_FILENAME
aws s3 ls $S3_FILENAME
