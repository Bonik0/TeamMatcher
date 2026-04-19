from redis import Redis


def get_redis_client() -> Redis:
    from core.models.redis import client

    return client
