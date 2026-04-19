from pydantic import BaseModel, EmailStr
from core.entities import UserRoleType, Role, Project


class FindUserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    patronymic: str | None
    surname: str
    role: UserRoleType


class FindProjectRoleOut(BaseModel):
    id: int

    description: str | None
    quantity_per_team: int

    role: Role


class FindTeamMemberOut(BaseModel):
    id: int
    competence_match: float
    role_score: float

    user: FindUserOut
    project_role: FindProjectRoleOut


class FindTeamOut(BaseModel):
    id: int
    name: str
    project: Project
    members: list[FindTeamMemberOut]


class FindUserTeamsOut(BaseModel):
    teams: list[FindTeamOut]
