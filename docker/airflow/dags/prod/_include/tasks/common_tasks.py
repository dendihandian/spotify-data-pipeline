from airflow.decorators import task
from _utils.redis.test_connection import ping
from _utils.spotify.test_connection import refresh_token
from airflow import AirflowException

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
