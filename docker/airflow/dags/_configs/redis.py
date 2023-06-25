from os import getenv

REDIS_CONFIG = {
    'host': getenv('REDIS_HOST', 'redis'),
    'port': getenv('REDIS_PORT', 6379),
    'pass': getenv('REDIS_PASS', None),
}