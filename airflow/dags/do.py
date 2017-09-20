import airflow
import datetime
from airflow.operators.python_operator import ShortCircuitOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import airflow.utils.helpers
import random

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
        dag_id='more',
        default_args=args,
        schedule_interval=datetime.timedelta(seconds=10)
        )

test = ShortCircuitOperator(
    task_id='test',
    python_callable=lambda: random.random() > 0.5,
    dag=dag)

node = DummyOperator(
        task_id='dosomething',
        dag=dag)

node.set_upstream(test)
