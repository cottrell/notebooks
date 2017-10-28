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
        python ${DIR}/trainer/task.py --filename=${FILENAME} \
            --maxlen=100 \
            --epochs=2 \
            --seq-length=10 \
            --hidden-dim=10
        ;;
    gcloud_local)
        gcloud ml-engine local train --package-path trainer \
                                     --module-name trainer.task \
                                     -- \
                                     --filename=${FILENAME} \
                                     --maxlen=100 \
                                     --epochs=2 \
                                     --seq-length=10 \
                                     --hidden-dim=10
        ;;
    gcloud_mlengine)
        # see readme for setup etc
        gcloud ml-engine jobs submit training ${JOB_NAME} \
                                     --package-path trainer \
                                     --module-name trainer.task \
                                     --staging-bucket gs://${BUCKET} \
                                     --job-dir gs://${BUCKET}/${JOB_NAME} \
                                     -- \
                                     --filename=${GCS_FILENAME} \
                                     --maxlen=100 \
                                     --epochs=2 \
                                     --seq-length=10 \
                                     --hidden-dim=10
        ;;
    *)
        echo unknown method ${method}
        ;;
esac
