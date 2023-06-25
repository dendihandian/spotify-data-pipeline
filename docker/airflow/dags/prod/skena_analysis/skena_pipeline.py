from datetime import datetime
from airflow import DAG
from prod.skena_analysis.skena_tasks import search_and_store_playlist

now = datetime.now()

default_args = {
    'start_date': datetime(now.year, now.month, now.day),
}

with DAG('skena_pipeline', default_args=default_args, schedule_interval='@daily') as dag:

    ingest_playlists = search_and_store_playlist.override(task_id='ingest_playlists')('skena')