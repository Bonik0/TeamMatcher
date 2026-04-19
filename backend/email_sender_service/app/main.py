from faststream import FastStream
from fastapi import Depends
from core.models.rabbitmq import rabbitmq_router
from app.verification_code.dependencies import get_verification_code_use_cases
from app.verification_code.use_cases import VerifyCodeEmailSendUseCase
from core.models.rabbitmq.email import simple_email_subscriber
from core.entities import VerificationCode


app = FastStream(rabbitmq_router.broker)


@simple_email_subscriber
async def send_verification_code(
    verification_code: VerificationCode,
    use_case: VerifyCodeEmailSendUseCase = Depends(get_verification_code_use_cases),
) -> None:
    await use_case.execute(verification_code)
