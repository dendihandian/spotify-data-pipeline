import requests
from _utils.redis.client import redis
from _configs.spotify import SPOTIFY_CONFIG

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

        rk_spotify_credential = 'spotify:credentials'
        redis.hset(rk_spotify_credential,'access_token', response_json['access_token'])
        redis.hset(rk_spotify_credential,'token_type', response_json['token_type'])
        redis.hset(rk_spotify_credential,'expires_in', response_json['expires_in'])
        redis.expire(rk_spotify_credential, int(response_json['expires_in']))

    else:
        return False

    return True
