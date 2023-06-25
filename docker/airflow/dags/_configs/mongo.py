from os import getenv

MONGO_CONFIG = {
    'host': getenv('MONGO_HOST', 'mongo'),
    'port': getenv('MONGO_PORT', 27017),
    'user': getenv('MONGO_USER', None),
    'pass': getenv('MONGO_PASS', None),
}