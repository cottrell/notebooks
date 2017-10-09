#!/bin/sh
conda env list | grep -s airflow || conda create --name airflow
source activate airflow
# https://issues.apache.org/jira/browse/AIRFLOW-1102
conda install -y pandas
pip install airflow git+git://github.com/deribit/deribit-api-python.git
pip uninstall -y gunicorn
pip install gunicorn==19.3.0
airflow initdb
