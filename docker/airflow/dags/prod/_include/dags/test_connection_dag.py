from datetime import datetime
from airflow import DAG
from prod._include.tasks.common_tasks import redis_test_connection
from airflow.decorators import task

now = datetime.now()

default_args = {
    'start_date': datetime(now.year, now.month, now.day),
}

with DAG('test_connection_dag', default_args=default_args, schedule_interval='@daily') as dag:

    redis_test = redis_test_connection.override(task_id='redis_test')()

    redis_test


"""
tasks list:
docker-compose exec airflow airflow tasks list test_connection_dag

dag test:
docker-compose exec airflow airflow dags test test_connection_dag 2023-01-01

dag run manually with executing the first task:
docker-compose exec airflow airflow tasks run test_connection_dag redis_test 2023-01-01

task test:
docker-compose exec airflow airflow tasks test test_connection_dag redis_test 2023-01-01
"""