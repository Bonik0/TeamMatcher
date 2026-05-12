from pydantic_settings import BaseSettings, SettingsConfigDict


class MatchSettings(BaseSettings):
    QUANTIZE: str
    LOW_LEVEL_VALUE: str
    MIDDLE_LEVEL_VALUE: str
    HIGH_LEVEL_VALUE: str
    DESIRDED_ROLE_COEFF: str
    ROLE_PRIORITY_BONUS_COEFF: str
    INITIAL_TEMPERATURE: float
    COOLING_RATE: float
    MINIMAL_TEMPERATURE: float
    STEPS_PER_TEMP_FACTOR: int
    RANDOM_SEED: int | None = None
    
    model_config = SettingsConfigDict(env_prefix="MATCH_", extra="ignore", frozen=True)


match_settings = MatchSettings()