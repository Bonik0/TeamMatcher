from pydantic import EmailStr, BaseModel
from enum import StrEnum, auto


class UserRoleType(StrEnum):
    user = auto()
    organizer = auto()


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    patronymic: str | None
    surname: str
    role: UserRoleType
    hash_password: str
