from pydantic import BaseModel
from enum import StrEnum
from datetime import datetime
from core.entities.base.user import UserRoleType


class JWTTokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class JWTTokenPayload(BaseModel):
    jti: str
    user_id: int
    device_id: str
    role: UserRoleType
    type: JWTTokenType
    exp: datetime
    iat: datetime
