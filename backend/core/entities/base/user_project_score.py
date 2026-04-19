from pydantic import BaseModel
from decimal import Decimal


class UserProjectScore(BaseModel):
    user_id: int
    project_role_id: int
    competence_match: Decimal
    role_score: Decimal
