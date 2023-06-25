import requests
from _utils.redis.client import redis
from _configs.spotify import SPOTIFY_CONFIG

sporify_api_base_url        = 'https://api.spotify.com/v1'
rediskey_spotify_credential = 'spotify:credentials'

#### LOW-LEVEL FUNCTIONS

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

def search_for_item(q, type=['playlist'], market=['ID'], limit=50, offset=0):

    token = get_access_token()

    response = requests.get(
        url=f"{sporify_api_base_url}/search",
        headers={
            'Authorization' : f'Bearer {token}',
        },
        params={
            'q'         : q,
            'type'      : ",".join(type),
            'market'    : ",".join(market),
            'limit'     : limit,
            'offset'    : offset,
        }
    )

    # print('response.status_code:', response.status_code)
    # print('response.status_code:', response.text)

    return response.json()

#### HIGH-LEVEL FUNCTIONS

def search_for_playlists(q, market=['ID']):

    limit           = 50
    offset          = 0
    offset_exceed   = False
    playlists       = []
    total           = None

    while not offset_exceed:

        response        = search_for_item(q, ['playlist'], market, limit=limit, offset=offset)
        total           = int(response['playlists']['total'])

        playlists       = playlists + response['playlists']['items']
        offset          = offset + limit
        offset_exceed   = True if (offset >= total) else False

    return playlists
