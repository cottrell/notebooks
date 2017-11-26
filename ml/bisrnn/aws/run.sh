#!/bin/bash -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${DIR}/env.sh
python ${DIR}/trainer/task.py run --filename=${FILENAME} \
    --maxlen=100 \
    --epochs=2 \
    --seq-length=10 \
    --hidden-dim=2 \
    --layer-num=2
