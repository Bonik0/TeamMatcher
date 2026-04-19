from pydantic_settings import SettingsConfigDict
from core.models.base import BaseSettings
from pydantic import Field
from functools import lru_cache


class RedisSettings(BaseSettings):
    DB: int = Field(default=0)

    model_config = SettingsConfigDict(env_prefix="REDIS_", extra="ignore", frozen=True)



def get_redis_settings() -> RedisSettings:
    return RedisSettings()


def get_redis_url() -> str:
    settings = get_redis_settings()
    return f'redis://:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB}'
