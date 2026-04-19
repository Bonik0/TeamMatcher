from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettings(BaseSettings):
    PASSWORD: str
    PORT: int
    HOST: str

    model_config = SettingsConfigDict(extra="ignore", frozen=True)
