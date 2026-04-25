from pydantic import PositiveInt, BaseModel


class SMTPSettings(BaseModel):
    SERVER: str
    PORT: PositiveInt
    LOGIN: str
    PASSWORD: str
