import redis

def get_redis_client():
    client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
    try:
        client.ping()
    except redis.ConnectionError:
        raise RuntimeError("Could not connect to Redis")
    return client

redis_client = get_redis_client()
