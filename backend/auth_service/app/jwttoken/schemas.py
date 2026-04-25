from core.schemas import BaseModel


class UpdateTokensIn(BaseModel):
    refresh_token: str
