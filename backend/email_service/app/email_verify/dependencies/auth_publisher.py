from functools import lru_cache
from faststream.rabbit.publisher import RabbitPublisher


@lru_cache
def get_auth_verify_publisher() -> RabbitPublisher:
    from core.models.rabbitmq.auth import auth_verify_publisher

    return auth_verify_publisher
