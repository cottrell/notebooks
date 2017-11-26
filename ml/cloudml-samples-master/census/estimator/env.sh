#!/bin/sh -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -e "$DIR/data" ]; then
	mkdir data
	gsutil -m cp gs://cloudml-public/census/data/* data/
fi
TRAIN_DATA=$DIR/data/adult.data.csv
EVAL_DATA=$DIR/data/adult.test.csv

[[ ${CONDA_DEFAULT_ENV} = py27 ]] || source ${HOME}/anaconda3/envs/36/bin/activate py27
touchfile=$DIR/pip.touch
if [[ ! -e $touchfile ]]; then
    pip install -r ../requirements.txt
    touch $touchfile
fi

MODEL_DIR=$DIR/output

method=noop
if [[ "$1" ]]; then
    method=$1
fi
case $method in
    local)
        gcloud ml-engine local train \
            --module-name trainer.task \
            --package-path trainer/ \
            -- \
            --train-files $TRAIN_DATA \
            --eval-files $EVAL_DATA \
            --train-steps 1000 \
            --job-dir $MODEL_DIR \
            --eval-steps 100 \
            --verbosity DEBUG
        ;;
    *)
        echo unknown method ${method}
        ;;
esac

