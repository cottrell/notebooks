#!/bin/sh
DIR="$( cd "$(dirname "$0")" ; pwd -P )"
. ${DIR}/env.sh
echo aws s3 ls s3://${BUCKET}/${GCS_FILENAME}
aws s3 ls s3://${BUCKET}/${GCS_FILENAME}
