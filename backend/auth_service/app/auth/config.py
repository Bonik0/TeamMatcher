from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta


class AuthtorizationSettings(BaseSettings):
    BLOCK_LIFETIME: timedelta

    model_config = SettingsConfigDict(env_prefix="AUTH_", extra="ignore", frozen=True)


auth_settings = AuthtorizationSettings()
