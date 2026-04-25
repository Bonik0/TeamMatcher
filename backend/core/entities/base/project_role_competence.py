from pydantic import Field, BaseModel


class ProjectRoleCompetence(BaseModel):
    project_role_id: int
    competence_id: int
    importance: int = Field(ge=1, le=10, description="Важность компетенции для роли")
