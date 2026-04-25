from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel


class ProjectStatus(StrEnum):
    RECRUITING = "recruiting"
    CANCELLED = "cancelled"
    FORMATED = "formated"
    COMPLETED = "completed"


class Project(BaseModel):
    id: int
    name: str
    description: str | None = None
    organizer_id: int
    status: ProjectStatus
    start_time: datetime
