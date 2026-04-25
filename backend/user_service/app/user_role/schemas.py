from pydantic import BaseModel, NonNegativeInt
from datetime import datetime
from core.entities import ProjectStatus, Role


class UserRoleIn(BaseModel):
    project_role_id: NonNegativeInt
    priority: int


class AddOrUpdateUserRoleIn(BaseModel):
    project_id: NonNegativeInt
    roles: list[UserRoleIn]


class DeleteUserProjectRolesIn(BaseModel):
    project_id: NonNegativeInt


class UserRoleOut(BaseModel):
    project_role_id: int
    priority: int


class FindUserRoleByIdOut(BaseModel):
    roles: list[UserRoleOut]


class ProjectRoleOut(BaseModel):
    id: int
    description: str | None
    quantity_per_team: int
    role: Role
    forms: list[UserRoleOut]


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    organizer_id: int
    status: ProjectStatus
    start_time: datetime
    user_forms_count: int
    roles: list[ProjectRoleOut]


class FindAllUserRolesOut(BaseModel):
    projects: list[ProjectOut]
