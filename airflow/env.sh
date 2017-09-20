export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export AIRFLOW_HOME=$DIR

# https://issues.apache.org/jira/browse/AIRFLOW-1102
# pip uninstall -y gunicorn
# pip install gunicorn==19.3.0
# airflow initdb
# airflow scheduler > $DIR/scheduler.log 2>&1
# airflow webserver > $DIR/webserver.log 2>&1
