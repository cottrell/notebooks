export DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export AIRFLOW_HOME=$DIR

# airflow initdb
# airflow scheduler > $DIR/scheduler.log 2>&1
# airflow webserver > $DIR/webserver.log 2>&1
