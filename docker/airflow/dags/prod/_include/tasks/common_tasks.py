from _utils.redis.test_connection import ping
from _utils.spotify.test_connection import refresh_token
from _utils.spotify.client import search_for_playlists
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
def search_and_store_playlist(q):
    playlist = search_for_playlists(q)

    print('playlist_len', len(playlist))