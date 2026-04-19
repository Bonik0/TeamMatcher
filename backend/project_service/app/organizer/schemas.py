from pydantic import (
    BaseModel,
    Field,
    model_validator,
    NonNegativeInt,
    PositiveInt,
    EmailStr,
)
from datetime import datetime
from core.entities import ProjectStatus, Role, Competence, Project, UserRoleType
from core.schemas import StrXSS


class CompetenceIn(BaseModel):
    name: StrXSS
    importance: int = Field(ge=0, le=10, description="Важность компетенции для роли")


class RoleIn(BaseModel):
    name: StrXSS
    description: StrXSS | None
    quantity_per_team: PositiveInt = Field(ge=1)
    competences: list[CompetenceIn] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_competences_names(self):
        competences_names = [competence.name for competence in self.competences]
        if len(set(competences_names)) != len(competences_names):
            raise ValueError("competencе cannot be included more than once")
        return self


class ProjectCreateIn(BaseModel):
    name: StrXSS = Field(max_length=255)
    description: StrXSS | None = None
    start_time: datetime
    roles: list[RoleIn] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_start_time(self):
        if self.start_time.timestamp() <= datetime.now().timestamp():
            raise ValueError("start_time must be in the future")
        return self

    @model_validator(mode="after")
    def validate_roles_names(self):
        roles_names = [role.name for role in self.roles]
        if len(set(roles_names)) != len(roles_names):
            raise ValueError("role cannot be included more than once")
        return self


class ProjectUpdateIn(ProjectCreateIn):
    project_id: NonNegativeInt


class ProjectCancelIn(BaseModel):
    project_id: NonNegativeInt


class ProjectFormatingIn(BaseModel):
    project_id: NonNegativeInt


class ProjectCreateOut(BaseModel):
    project_id: NonNegativeInt


class ProjectRoleCompetenceOut(BaseModel):
    importance: int = Field(ge=0, le=10, description="Важность компетенции для роли")
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
    organizer_id: int
    status: ProjectStatus
    start_time: datetime
    user_forms_count: int
    roles: list[ProjectRoleOut]


class ProjectFindOut(BaseModel):
    projects: list[ProjectOut]


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
    competence_match: float
    role_score: float

    user: FindUserOut


class FindTeamOut(BaseModel):
    id: int
    name: str
    members: list[FindTeamMemberOut]


class FindProjectWithTeamsOut(Project):
    roles: list[FindProjectRoleOut]
    teams: list[FindTeamOut]


class FindOrganizerTeamsOut(BaseModel):
    projects: list[FindProjectWithTeamsOut]
