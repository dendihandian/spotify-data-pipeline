from _utils.redis.test_connection import ping
from _utils.spotify.test_connection import refresh_token
from _utils.mongo.test_connection import get_test_database
from airflow import AirflowException
from airflow.decorators import task

@task
def redis_test_connection():
    if (ping()):
        print('redis_connected')
    else:
        raise AirflowException('redis_disconnected')

@task
def spotify_test_connection():
    if (refresh_token()):
        print('spotify_connected')
    else:
        raise AirflowException('spotify_disconnected')

@task
def mongo_test_connection():
    if (get_test_database()):
        print('mongo_connected')
    else:
        raise AirflowException('mongo_disconnected')
