from datetime import datetime
from airflow import DAG
from prod.skena_analysis.skena_tasks import ingest_playlists, get_tracks_from_playlists

now = datetime.now()

default_args = {
    'start_date': datetime(now.year, now.month, now.day),
}

with DAG('skena_pipeline', default_args=default_args, schedule_interval='@daily') as dag:

    get_tracks_from_playlists(ingest_playlists('skena'))