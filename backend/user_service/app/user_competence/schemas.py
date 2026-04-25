from pydantic import BaseModel, NonNegativeInt
from core.entities import UserCompetenceLevelType, Competence


class UserCompetenceIn(BaseModel):
    competence_id: NonNegativeInt
    level: UserCompetenceLevelType


class AddOrUpdateUserCompetenceIn(BaseModel):
    competences: list[UserCompetenceIn]


class RemoveUserCompetenceIn(BaseModel):
    competence_ids: list[NonNegativeInt]


class UserCompetenceOut(BaseModel):
    level: UserCompetenceLevelType
    competence: Competence


class UserCompetencesOut(BaseModel):
    competences: list[UserCompetenceOut]
