#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${DIR}/env.sh
method=python_local
if [[ "$1" ]]; then
    method=$1
fi
echo method=${method}
case $method in
    python_local)
        # max len is total data size
        python ${DIR}/trainer/task.py run --filename=${FILENAME} \
            --maxlen=100 \
            --epochs=2 \
            --seq-length=10 \
            --hidden-dim=2 \
            --layer-num=2
        ;;
    gcloud_local)
        gcloud ml-engine local train --package-path trainer \
                                     --module-name trainer.task \
                                     -- \
                                     run \
                                     --filename=${FILENAME} \
                                     --maxlen=100 \
                                     --epochs=2 \
                                     --seq-length=10 \
                                     --layer-num=2 \
                                     --hidden-dim=2
        ;;
    gcloud_mlengine)
        # see readme for setup etc
        gcloud ml-engine jobs submit training ${JOB_NAME} \
                                     --package-path trainer \
                                     --module-name trainer.task \
                                     --staging-bucket gs://${BUCKET} \
                                     --job-dir gs://${BUCKET}/${JOB_NAME} \
                                     -- \
                                     run \
                                     --filename=${GCS_FILENAME} \
                                     --batch-size=50 \
                                     --layer-num=2 \
                                     --seq-length=10 \
                                     --hidden-dim=2 \
                                     --generate-length=2 \
                                     --epochs=2 \
                                     --maxlen=100
        ;;
    *)
        echo unknown method ${method}
        ;;
esac
