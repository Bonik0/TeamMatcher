from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PositiveInt
from datetime import timedelta
from functools import lru_cache


class ServiceSettings(BaseSettings):
    CODE_MAX_FAIL_ATTEMPT_COUNT: PositiveInt
    CODE_LENGTH: PositiveInt
    CODE_LIFETIME: timedelta

    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="VERIFY_EMAIL_",
        env_nested_delimiter="_",
        frozen=True,
    )


@lru_cache
def get_service_settings() -> ServiceSettings:
    return ServiceSettings()
