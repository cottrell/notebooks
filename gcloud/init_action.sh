#!/bin/sh

# gsutil cp init_action.sh gs://misc-data-ml/init_action.sh

pip install --upgrade pip
pip install argh pandas xgboost pyarrow keras tensorflow
