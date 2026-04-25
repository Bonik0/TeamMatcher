from pydantic import Field, ConfigDict
from .base import BaseModel
from enum import StrEnum, auto


class SuccessUserActionStatusType(StrEnum):
    SUCCESS = auto()
    SUCCESS_INSERT = auto()
    SUCCESS_UPDATE = auto()
    SUCCESS_DELETE = auto()


class UserActionOut(BaseModel):
    status: SuccessUserActionStatusType = Field(
        default=SuccessUserActionStatusType.SUCCESS, description="Change status"
    )

    model_config = ConfigDict(title="Successful completion")


class InsertUserActionOut(UserActionOut):
    status: SuccessUserActionStatusType = Field(
        default=SuccessUserActionStatusType.SUCCESS_INSERT
    )


class UpdateUserActionOut(UserActionOut):
    status: SuccessUserActionStatusType = Field(
        default=SuccessUserActionStatusType.SUCCESS_UPDATE
    )


class DeleteUserActionOut(UserActionOut):
    status: SuccessUserActionStatusType = Field(
        default=SuccessUserActionStatusType.SUCCESS_DELETE
    )
