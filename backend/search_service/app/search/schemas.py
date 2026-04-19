from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt
from core.entities import Role, Competence, ProjectStatus
from datetime import datetime


class FindIn(BaseModel):
    limit: PositiveInt = Field(default=100, le=100)
    offset: NonNegativeInt = Field(default=0)
    q: str | None = None


class FindRoleIn(FindIn):
    pass


class FindCompetenceIn(FindIn):
    pass


class FindRoleOut(BaseModel):
    roles: list[Role]


class FindCompetenceOut(BaseModel):
    competencies: list[Competence]


class FindProjectIn(FindIn):
    role_ids: list[NonNegativeInt] | None = None
    competence_ids: list[NonNegativeInt] | None = None


class ProjectRoleCompetenceOut(BaseModel):
    competence: Competence


class ProjectRoleOut(BaseModel):
    id: int
    description: str | None
    quantity_per_team: int
    role: Role
    competences: list[ProjectRoleCompetenceOut]


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    status: ProjectStatus
    start_time: datetime
    user_forms_count: int
    roles: list[ProjectRoleOut]


class FindProjectOut(BaseModel):
    projects: list[ProjectOut]
