import requests
from _utils.redis.client import redis
from _configs.spotify import SPOTIFY_CONFIG
import json
import uuid
from time import sleep

spotify_api_base_url        = 'https://api.spotify.com/v1'
rediskey_spotify_credential = 'spotify:credentials'

plurals = {
    'playlist'  : 'playlists',
    'track'     : 'tracks',
}

#### LOW-LEVEL FUNCTIONS

def getter(url_path, token, params):
    return requests.get(spotify_api_base_url + url_path, headers={'Authorization' : f'Bearer {token}'}, params=params)

def request_access_token():
    response = requests.post(
        url='https://accounts.spotify.com/api/token',
        headers={
            'Content-Type' : 'application/x-www-form-urlencoded',
        },
        data={
            'grant_type'    : 'client_credentials',
            'client_id'     : SPOTIFY_CONFIG['client_id'],
            'client_secret' : SPOTIFY_CONFIG['client_secret'],
        }
    )

    return response

def refresh_access_token():

    response = request_access_token()

    if (int(response.status_code) == 200):

        response_json = response.json()

        redis.hset(rediskey_spotify_credential,'access_token', response_json['access_token'])
        redis.hset(rediskey_spotify_credential,'token_type', response_json['token_type'])
        redis.hset(rediskey_spotify_credential,'expires_in', response_json['expires_in'])
        redis.expire(rediskey_spotify_credential, int(response_json['expires_in']))

    else:
        return False

    return True

def get_access_token():

    if not redis.hexists(rediskey_spotify_credential, 'access_token'):
        response = refresh_access_token()

    return redis.hget(rediskey_spotify_credential, 'access_token')

### API FUNCTIONS

def search_for_item(q, search_type='playlist', market=['ID'], delay=0):

    _search_type    = search_type
    _market         = ",".join(list(set(sorted(market))))
    cache_hash      = str(uuid.uuid5(uuid.NAMESPACE_DNS, q+_search_type+_market))
    cache_key       = f'spotify:api-cache:search_for_item:{cache_hash}'

    if redis.exists(cache_key):
        return json.loads(redis.get(cache_key))

    token   = get_access_token()
    items  = []

    limit           = 50
    offset          = 0
    offset_exceed   = False
    total           = None

    while not offset_exceed:
        response        = getter(f"/search", token, params={'q':q, 'type':_search_type, 'market':_market, 'limit':limit, 'offset':offset})
        response_json   = response.json()

        total           = int(response_json[plurals[search_type]]['total'])
        items           = items + response_json[plurals[search_type]]['items']
        offset          = offset + limit
        offset_exceed   = True if (offset >= total) else False

    redis.set(cache_key, json.dumps(items), 3600)
    sleep(delay)

    return items

def get_playlist_tracks(playlist_id, market=['ID'], fields='', delay=0):

    _market     = "-".join(list(set(sorted(market))))
    _fields     = fields
    cache_hash  = str(uuid.uuid5(uuid.NAMESPACE_DNS, playlist_id+_market+_fields))
    cache_key   = f'spotify:api-cache:get_playlist_tracks:{cache_hash}'

    if redis.exists(cache_key):
        return json.loads(redis.get(cache_key))

    token   = get_access_token()
    tracks  = []

    limit           = 50
    offset          = 0
    offset_exceed   = False
    total           = None

    while not offset_exceed:
        response        = getter(f"/playlists/{playlist_id}/tracks", token, params={'market':",".join(market), 'fields':fields, 'limit':limit, 'offset':offset})
        response_json   = response.json()

        total           = int(response_json['total'])
        tracks          = tracks + response_json['items']
        offset          = offset + limit
        offset_exceed   = True if (offset >= total) else False

    redis.set(cache_key, json.dumps(tracks), 86400)
    sleep(delay)

    return tracks
