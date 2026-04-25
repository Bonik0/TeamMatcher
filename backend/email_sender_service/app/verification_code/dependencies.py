from app.verification_code.config import get_service_settings, VerificationCodeSettings
from fastapi import Depends
from app.verification_code.use_cases import VerifyCodeEmailSendUseCase


def get_verification_code_use_cases(
    settings: VerificationCodeSettings = Depends(get_service_settings),
) -> VerifyCodeEmailSendUseCase:
    return VerifyCodeEmailSendUseCase(
        server=settings.SMTP.SERVER,
        port=settings.SMTP.PORT,
        login=settings.SMTP.LOGIN,
        password=settings.SMTP.PASSWORD,
        page_url=settings.CODE_PAGE_URL,
    )
