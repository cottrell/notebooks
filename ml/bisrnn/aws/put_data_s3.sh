#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${DIR}/env.sh
aws s3 cp ${LOCAL_FILENAME} ${S3_FILENAME}
