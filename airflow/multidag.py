"""
Example DAG showing how to create multi dags dinamically in a single file,
using python globals().
"""

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator


args = {
    'owner': 'ap3x',
    'start_date': airflow.utils.dates.days_ago(1),
}


for code in range(5):
    globals()[f'dag_{code}'] = DAG(
        dag_id=f'dag_{code}',
        default_args=args,
        schedule_interval='0/10 * * * *')

    globals()[f'start_task_{code}'] = DummyOperator(
        dag=globals()[f'dag_{code}'],
        task_id=f'start_task')

    globals()[f'end_task_{code}'] = DummyOperator(
        dag=globals()[f'dag_{code}'],
        task_id=f'end_task')

    globals()[f'start_task_{code}'] >> globals()[f'end_task_{code}']
