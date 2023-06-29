from _utils.mongo.client import mongo
from _utils.spotify.client import search_for_item, get_playlist_tracks
from airflow.decorators import task
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
import pprint
import time

@task
def ingest_playlists(q):

    skena_analysis = mongo['skena_analysis']
    raw_playlists = skena_analysis["raw_playlists"]

    playlists = search_for_item(q, search_type='playlist', market=['ID'])
    print('FYI len(playlists)', len(playlists))

    for index, playlist in enumerate(playlists):
        playlists[index]['_id'] = playlist['id']

    upsert_requests = [UpdateOne({'_id': playlist['_id']}, {'$set': playlist}, upsert=True) for playlist in playlists]
    playlists_ids = [playlist['_id'] for playlist in playlists]

    try:

        result = raw_playlists.bulk_write(upsert_requests)
        print(f"FYI Upserted documents: {result.upserted_count}")
        print(f"FYI Modified documents: {result.modified_count}")

    except BulkWriteError as bwe:
        pprint(bwe.details)

    return playlists_ids

@task
def get_tracks_from_playlists(playlist_ids):

    playlists_tracks = {}

    if len(playlist_ids) > 0:

        for playlist_id in playlist_ids:
            tracks = get_playlist_tracks(playlist_id, market=['ID'], delay=5)
            playlists_tracks[playlist_id] = tracks

        if len(playlists_tracks.keys()) > 0:
            raw_playlists_tracks = mongo['skena_analysis']['raw_playlists_tracks']
            upsert_requests = [UpdateOne({'_id': playlist_id['_id']}, {'$set': playlists_tracks[playlist_id]}, upsert=True) for playlist_id in playlists_tracks.keys()]

            try:

                result = raw_playlists_tracks.bulk_write(upsert_requests)
                print(f"FYI Upserted documents: {result.upserted_count}")
                print(f"FYI Modified documents: {result.modified_count}")

            except BulkWriteError as bwe:
                pprint(bwe.details)

    return playlists_tracks
