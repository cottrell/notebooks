#!/bin/bash -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${DIR}/env.sh
python ${DIR}/trainer/task.py run --filename=${FILENAME} \
    --maxlen=57000000 \
    --epochs=1000 \
    --seq-length=1000 \
    --hidden-dim=5 \
    --layer-num=5 \
    --batch-size=500 \
    --generate-length=1000

