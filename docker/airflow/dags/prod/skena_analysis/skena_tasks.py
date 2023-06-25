from _utils.mongo.client import mongo
from _utils.spotify.client import search_for_playlists
from airflow.decorators import task
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
import pprint

@task
def search_and_store_playlist(q):

    skena_analysis = mongo['skena_analysis']
    raw_playlists = skena_analysis["raw_playlists"]

    playlists = search_for_playlists(q)
    print('FYI len(playlists)', len(playlists))

    for index, playlist in enumerate(playlists):
        playlists[index]['_id'] = playlist['id']

    upsert_requests = [UpdateOne({'_id': playlist['_id']}, {'$set':playlist}, upsert=True) for playlist in playlists]

    try:

        result = raw_playlists.bulk_write(upsert_requests)
        print(f"FYI Upserted documents: {result.upserted_count}")
        print(f"FYI Modified documents: {result.modified_count}")

        # TODO: push to xcom for transform task
        # upserted_ids = upserted_ids.values()

    except BulkWriteError as bwe:
        pprint(bwe.details)

