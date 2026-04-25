from pydantic import BaseModel


class ProjectRole(BaseModel):
    id: int

    project_id: int
    role_id: int
    description: str | None
    quantity_per_team: int
