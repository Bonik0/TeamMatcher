from pydantic import BaseModel
from enum import IntEnum


class UserCompetenceLevelType(IntEnum):
    LOW = 1
    MIDDLE = 2
    HIGH = 3


class UserCompetence(BaseModel):
    user_id: int
    competence_id: int

    level: UserCompetenceLevelType
