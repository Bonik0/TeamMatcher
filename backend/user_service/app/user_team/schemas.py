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
    project_role_id: int
    user: FindUserOut


class FindTeamOut(BaseModel):
    id: int
    name: str
    members: list[FindTeamMemberOut]


class FindProjectWithTeamsOut(Project):
    roles: list[FindProjectRoleOut]
    teams: list[FindTeamOut]


class FindUserTeamsOut(BaseModel):
    projects: list[FindProjectWithTeamsOut]
