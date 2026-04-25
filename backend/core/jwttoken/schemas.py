from pydantic import Field, ConfigDict, BaseModel
from typing import Annotated, TypeAlias
from fastapi import Security
from fastapi.security import APIKeyHeader


class IssuedJWTTokensOut(BaseModel):
    access_token: str = Field(description="access_token")
    refresh_token: str = Field(description="refresh_token")
    exp: float = Field(description="Lifetime access_token")

    model_config = ConfigDict(title="Generated access_token and refresh_token")


AuthAPIHeaderIn: TypeAlias = Annotated[
    str | None,
    Security(
        APIKeyHeader(
            name="Authorization", auto_error=False, scheme_name="User Authorization"
        )
    ),
]
