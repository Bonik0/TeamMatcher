from pydantic_settings import SettingsConfigDict
from core.models.base import BaseSettings
from functools import lru_cache


class RabbitMQSettings(BaseSettings):
    USER: str
    VHOST: str

    model_config = SettingsConfigDict(
        env_prefix="RABBITMQ_", extra="ignore", frozen=True
    )


@lru_cache()
def get_url() -> str:
    rabbitmq_settings = RabbitMQSettings()
    return (
        f"amqp://{rabbitmq_settings.USER}:{rabbitmq_settings.PASSWORD}"
        f"@{rabbitmq_settings.HOST}:{rabbitmq_settings.PORT}/{rabbitmq_settings.VHOST}"
    )
