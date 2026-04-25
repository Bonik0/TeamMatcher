from pydantic import BaseModel


class Team(BaseModel):
    id: int
    name: str
    project_id: int
