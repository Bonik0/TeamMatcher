from core.schemas import BaseModel
from pydantic import EmailStr, Field, ConfigDict, PositiveInt
from uuid import UUID


class SendEmailIn(BaseModel):
    email: EmailStr = Field(description="email for send verify mail")
    model_config = ConfigDict(title="form for send verify mail")


class OperationIDModel(BaseModel):
    operation_id: UUID = Field(description="Use this for validate your email in auth")


class SendEmailOut(OperationIDModel):
    pass


class VerifyCodeIn(OperationIDModel, BaseModel):
    code: PositiveInt = Field(description="mail code")
    email: EmailStr = Field(description="email")
    model_config = ConfigDict(title="code verification form")


class VerifyCodeOut(BaseModel):
    is_correct_code: bool
