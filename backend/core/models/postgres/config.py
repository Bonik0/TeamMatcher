from pydantic_settings import SettingsConfigDict
from core.models.base import BaseSettings
from functools import lru_cache


class PostgresSettings(BaseSettings):
    DB: str
    USER: str

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_", extra="ignore", frozen=True
    )


@lru_cache()
def get_db_url() -> str:
    postgres_settings = PostgresSettings()
    return (
        "postgresql+asyncpg://"
        f"{postgres_settings.USER}:{postgres_settings.PASSWORD}@"
        f"{postgres_settings.HOST}:{postgres_settings.PORT}/{postgres_settings.DB}"
    )
