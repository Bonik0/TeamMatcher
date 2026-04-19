from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta


class MatchSettings(BaseSettings):
    QUANTIZE: str
    LOW_LEVEL_VALUE: str
    MIDDLE_LEVEL_VALUE: str
    HIGH_LEVEL_VALUE: str
    DESIRDED_ROLE_COEFF: str
    ROLE_PRIORITY_BONUS_COEFF: str
    model_config = SettingsConfigDict(env_prefix="MATCH_", extra="ignore", frozen=True)


match_settings = MatchSettings()
