from pydantic import BaseModel


class UserProjectRole(BaseModel):
    user_id: int
    project_role_id: int
    priority: int
