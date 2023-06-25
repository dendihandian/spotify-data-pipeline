from _utils.redis.client import redis

def ping():
    return redis.ping()

if __name__ == '__main__':
    print(ping())
