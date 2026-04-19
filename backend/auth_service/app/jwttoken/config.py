from datetime import timedelta
from pydantic_settings import SettingsConfigDict, BaseSettings


class JWTTokenSettings(BaseSettings):
    SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_TTL: timedelta
    REFRESH_TOKEN_TTL: timedelta

    model_config = SettingsConfigDict(
        env_prefix="JWTTOKEN_", extra="ignore", frozen=True
    )


def get_jwt_token_settings() -> JWTTokenSettings:
    return JWTTokenSettings()
