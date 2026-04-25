from pydantic import Field, ConfigDict, EmailStr
from core.schemas import BaseModel, Str, StrXSS
from uuid import UUID


class LoginUserIn(BaseModel):
    email: EmailStr


class UserCredentialsIn(BaseModel):
    password: Str = Field(
        exclude=True, min_length=5, max_length=50, description="Password"
    )


class UserVerifyAccessIn(BaseModel):
    operation_id: UUID


class UserRegistrationCredentialsIn(UserCredentialsIn, LoginUserIn, UserVerifyAccessIn):
    first_name: StrXSS
    patronymic: StrXSS | None
    surname: StrXSS


class UserLoginCredentialsIn(UserCredentialsIn, LoginUserIn):
    model_config = ConfigDict(title="Logining to the account")


class UserChangePasswordIn(UserCredentialsIn, LoginUserIn, UserVerifyAccessIn):
    pass
