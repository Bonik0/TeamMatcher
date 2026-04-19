from pydantic import BaseModel


class Competence(BaseModel):
    id: int
    name: str
