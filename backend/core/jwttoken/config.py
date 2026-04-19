from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class AuthtorizationServiceSettings(BaseSettings):
    URL: str
    METHOD: str

    model_config = SettingsConfigDict(
        env_prefix="AUTH_SERVICE_", extra="ignore", frozen=True
    )


@lru_cache()
def get_auth_service_settings() -> AuthtorizationServiceSettings:
    return AuthtorizationServiceSettings()
