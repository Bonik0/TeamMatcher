from core.models.rabbitmq.auth import auth_verify_subscriber
from fastapi import Depends
from core.entities import VerificationCode
from app.user_verify.use_cases.save_case import SaveUserVerificationUseCase
from app.user_verify.dependencies.use_cases import get_save_use_case
from core.models.rabbitmq import rabbitmq_router


router = rabbitmq_router


@auth_verify_subscriber
async def accept_user_email_verification(
    code: VerificationCode,
    save_use_case: SaveUserVerificationUseCase = Depends(get_save_use_case),
) -> None:
    await save_use_case.execute(code.email, code.operation_id)


__all__ = ["router"]
