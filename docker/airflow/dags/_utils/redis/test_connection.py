from _utils.redis.client import redis

def ping():
    return redis.ping()


if __name__ == '__main__':

    print(ping())

"""
docker-compose exec airflow python /opt/airflow/dags/_utils/redis/test_connection.py
"""