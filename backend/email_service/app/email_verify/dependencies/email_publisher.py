from functools import lru_cache
from faststream.rabbit.publisher import RabbitPublisher


@lru_cache
def get_verification_code_publisher() -> RabbitPublisher:
    from core.models.rabbitmq.email import simple_email_publisher

    return simple_email_publisher
