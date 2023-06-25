from os import getenv

SPOTIFY_CONFIG = {
    'client_id': getenv('SPOTIFY_CLIENT_ID', ''),
    'client_secret': getenv('SPOTIFY_CLIENT_SECRET', ''),
}
