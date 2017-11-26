#!/bin/sh -e
# a script as notes from: https://cloud.google.com/ml-engine/docs/getting-started-training-prediction

# --scale-tier Enums
# BASIC	A single worker instance. This tier is suitable for learning how to use Cloud ML, and for experimenting with new models using small datasets.
# STANDARD_1	Many workers and a few parameter servers.
# PREMIUM_1	A large number of workers with many parameter servers.
# BASIC_GPU	A single worker instance with a GPU.
# BASIC_TPU	A single worker instance with a Cloud TPU
# CUSTOM
# The CUSTOM tier is not a set tier, but rather enables you to use your own cluster specification. When you use this tier, set values to configure your processing cluster according to these guidelines:
#
# You must set TrainingInput.masterType to specify the type of machine to use for your master node. This is the only required setting.
# You may set TrainingInput.workerCount to specify the number of workers to use. If you specify one or more workers, you must also set TrainingInput.workerType to specify the type of machine to use for your worker nodes.
# You may set TrainingInput.parameterServerCount to specify the number of parameter servers to use. If you specify one or more parameter servers, you must also set TrainingInput.parameterServerType to specify the type of machine to use for your parameter servers.
# Note that all of your workers must use the same machine type, which can be different from your parameter server type and master type. Your parameter servers must likewise use the same machine type, which can be different from your worker type and master type.

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

PROJECT_ID=$(gcloud config list project --format "value(core.project)")
BUCKET_NAME=${PROJECT_ID}-mlengine
REGION=$(gcloud config list --format "value(compute.region)")

method=noop
if [[ "$1" ]]; then
    method=$1
fi
case $method in
    local)
        OUTPUT_PATH=$DIR/output
        echo OUTPUT_PATH=$OUTPUT_PATH
        echo python -m tensorflow.tensorboard --logdir=$OUTPUT_PATH
        gcloud ml-engine local train \
            --module-name trainer.task \
            --package-path trainer/ \
            -- \
            --train-files $TRAIN_DATA \
            --eval-files $EVAL_DATA \
            --train-steps 1000 \
            --job-dir $OUTPUT_PATH \
            --eval-steps 100 \
            --verbosity DEBUG
        ;;
    distributed)
        # this is local? not sure what the difference is. maybe some tests?
        # From the help:
        #          --distributed
        #     Runs the provided code in distributed mode by providing cluster
        #     configurations as environment variables to subprocesses
        OUTPUT_PATH=output-dist
        echo OUTPUT_PATH=$OUTPUT_PATH
        echo python -m tensorflow.tensorboard --logdir=$OUTPUT_PATH
        gcloud ml-engine local train \
            --module-name trainer.task \
            --package-path trainer/ \
            --distributed \
            -- \
            --train-files $TRAIN_DATA \
            --eval-files $EVAL_DATA \
            --train-steps 1000 \
            --job-dir $OUTPUT_PATH # confusing but this is actually part of the task.py in local mode
        ;;
    upload_data)
        gsutil cp -r data gs://$BUCKET_NAME/data
        gsutil cp ../test.json gs://$BUCKET_NAME/data/test.json
        ;;
    cloud)
        TRAIN_DATA=gs://$BUCKET_NAME/data/adult.data.csv
        EVAL_DATA=gs://$BUCKET_NAME/data/adult.test.csv
        TEST_JSON=gs://$BUCKET_NAME/data/test.json
        JOB_NAME=census_single_1
        OUTPUT_PATH=gs://$BUCKET_NAME/$JOB_NAME
        echo OUTPUT_PATH=$OUTPUT_PATH
        echo you might need to run this first: gcloud auth application-default login
        echo will save creds to /Users/davidcottrell/.config/gcloud/application_default_credentials.json
        echo python -m tensorflow.tensorboard --logdir=$OUTPUT_PATH
        gcloud ml-engine jobs submit training $JOB_NAME \
            --job-dir $OUTPUT_PATH \
            --runtime-version 1.2 \
            --module-name trainer.task \
            --package-path trainer/ \
            --region $REGION \
            --scale-tier BASIC \
            -- \
            --train-files $TRAIN_DATA \
            --eval-files $EVAL_DATA \
            --train-steps 1000 \
            --verbosity DEBUG
        # success looks like this:
        # Job [census_single_1] submitted successfully.
        # Your job is still active. You may view the status of your job with the command
        #
        #   $ gcloud ml-engine jobs describe census_single_1
        #
        # or continue streaming the logs with the command
        #
        #   $ gcloud ml-engine jobs stream-logs census_single_1
        # jobId: census_single_1
        # state: QUEUED
        ;;
    cloud_distributed)
        TRAIN_DATA=gs://$BUCKET_NAME/data/adult.data.csv
        EVAL_DATA=gs://$BUCKET_NAME/data/adult.test.csv
        TEST_JSON=gs://$BUCKET_NAME/data/test.json
        JOB_NAME=census_dist_1
        OUTPUT_PATH=gs://$BUCKET_NAME/$JOB_NAME
        echo OUTPUT_PATH=$OUTPUT_PATH
        echo you might need to run this first: gcloud auth application-default login
        echo will save creds to /Users/davidcottrell/.config/gcloud/application_default_credentials.json
        echo python -m tensorflow.tensorboard --logdir=$OUTPUT_PATH
        gcloud ml-engine jobs submit training $JOB_NAME \
            --job-dir $OUTPUT_PATH \
            --runtime-version 1.2 \
            --module-name trainer.task \
            --package-path trainer/ \
            --region $REGION \
            --scale-tier STANDARD_1 \
            -- \
            --train-files $TRAIN_DATA \
            --eval-files $EVAL_DATA \
            --train-steps 1000 \
            --verbosity DEBUG \
            --eval-steps 100
        ;;
    cloud_tuning)
        HPTUNING_CONFIG=../hptuning_config.yaml
        JOB_NAME=census_core_hptune_1
        OUTPUT_PATH=gs://$BUCKET_NAME/$JOB_NAME
        echo OUTPUT_PATH=$OUTPUT_PATH
        echo you might need to run this first: gcloud auth application-default login
        echo will save creds to /Users/davidcottrell/.config/gcloud/application_default_credentials.json
        echo python -m tensorflow.tensorboard --logdir=$OUTPUT_PATH
        gcloud ml-engine jobs submit training $JOB_NAME \
            --stream-logs \
            --job-dir $OUTPUT_PATH \
            --runtime-version 1.2 \
            --config $HPTUNING_CONFIG \
            --module-name trainer.task \
            --package-path trainer/ \
            --region $REGION \
            --scale-tier STANDARD_1 \
            -- \
            --train-files $TRAIN_DATA \
            --eval-files $EVAL_DATA \
            --train-steps 1000 \
            --verbosity DEBUG  \
            --eval-steps 100
        ;;
    deploy_model)
        # deploy a trained model for prediction
        MODEL_NAME=census
        # gcloud ml-engine models list
        gcloud ml-engine models create $MODEL_NAME --regions=$REGION
        OUTPUT_PATH=gs://$BUCKET_NAME/census_dist_1
        # gsutil ls -r $OUTPUT_PATH/export # run this to find timestamp in next line
        MODEL_BINARIES=gs://$BUCKET_NAME/census_dist_1/export/Servo/1511705712/
        gcloud ml-engine versions create v1 \
            --model $MODEL_NAME \
            --origin $MODEL_BINARIES \
            --runtime-version 1.2
        ;;
    predict)
        echo predict
        # get a prediction from the deployed model
        MODEL_NAME=census
        gcloud ml-engine predict \
            --model $MODEL_NAME \
            --version v1 \
            --json-instances \
            ../test.json
        ;;
    predict_batch)
        # batch prediction (slow etc)
        MODEL_NAME=census
        JOB_NAME=census_prediction_1
        OUTPUT_PATH=gs://$BUCKET_NAME/$JOB_NAME
        gsutil ls gs://$BUCKET_NAME/data/test.json >/dev/null 2>&1 || gsutil cp ../test.json gs://$BUCKET_NAME/data/
        TEST_JSON=gs://$BUCKET_NAME/data/test.json
        gcloud ml-engine jobs submit prediction $JOB_NAME \
            --model $MODEL_NAME \
            --version v1 \
            --data-format TEXT \
            --region $REGION \
            --input-paths $TEST_JSON \
            --output-path $OUTPUT_PATH/predictions
        echo check with: gcloud ml-engine jobs describe $JOB_NAME
        echo check with: gsutil cat $OUTPUT_PATH/predictions/prediction.results-00000-of-00001
        ;;
    clean_bucket)
        for x in $(gsutil ls gs://$BUCKET_NAME/); do
            read -r -p "delete $x? [y/N] " response
            if [[ "$response" = "y" ]]; then
                echo deleting $x
                echo gsutil rm -r $x
            fi
        done
        ;;
    *)
        echo unknown method ${method}
        ;;
esac

