from redis import Redis
from configs.redis import REDIS_CONFIG

REDIS_HOST=REDIS_CONFIG['host']
REDIS_PORT=REDIS_CONFIG['port']
REDIS_AUTH=REDIS_CONFIG['pass']

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_AUTH, charset="utf-8", decode_responses=True)