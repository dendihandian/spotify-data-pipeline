from _utils.spotify.client import search_for_playlists
from airflow.decorators import task

@task
def search_and_store_playlist(q):
    playlist = search_for_playlists(q)
    print('playlist_len', len(playlist))