from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta


class VerificationSettings(BaseSettings):
    LIFETIME: timedelta

    model_config = SettingsConfigDict(
        env_prefix="VERIFICATE_", extra="ignore", frozen=True
    )


def get_verification_settings() -> VerificationSettings:
    return VerificationSettings()
