from pydantic_settings import BaseSettings, SettingsConfigDict
from app.base.config import SMTPSettings


class VerificationCodeSettings(BaseSettings):
    SMTP: SMTPSettings
    CODE_PAGE_URL: str

    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="VERIFY_EMAIL_",
        env_nested_delimiter="_",
        frozen=True,
    )


def get_service_settings() -> VerificationCodeSettings:
    return VerificationCodeSettings()
