#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${DIR}/env.sh
gsutil cp ${FILENAME} gs://${BUCKET}
