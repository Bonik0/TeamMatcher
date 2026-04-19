from pydantic import BaseModel


class TeamMember(BaseModel):
    id: int
    team_id: int
    user_id: int
    project_role_id: int
    competence_match: float
    role_score: float
