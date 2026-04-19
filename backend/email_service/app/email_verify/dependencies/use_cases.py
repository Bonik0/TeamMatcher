from core.dependencies.repositories.verification_code import (
    get_verification_code_reposirory,
)
from core.interfaces.repositories.verification_code import IVerificationRepository
from fastapi import Depends
from app.email_verify.use_cases.save_code import SaveVerificationCodeUseCase
from app.email_verify.config import get_service_settings, ServiceSettings
from app.email_verify.use_cases.verify_code import VerifyCodeUseCase
from app.email_verify.dependencies.email_publisher import (
    get_verification_code_publisher,
)
from app.email_verify.dependencies.auth_publisher import get_auth_verify_publisher
from faststream.rabbit.publisher import RabbitPublisher
from app.email_verify.use_cases.success_verify import SuccessVerifyUseCase


def get_save_code_use_case(
    repository: IVerificationRepository = Depends(get_verification_code_reposirory),
    publisher: RabbitPublisher = Depends(get_verification_code_publisher),
    settings: ServiceSettings = Depends(get_service_settings),
) -> SaveVerificationCodeUseCase:
    return SaveVerificationCodeUseCase(repository, publisher, settings.CODE_LIFETIME)


def get_verify_code_use_case(
    repository: IVerificationRepository = Depends(get_verification_code_reposirory),
    settings: ServiceSettings = Depends(get_service_settings),
) -> VerifyCodeUseCase:
    return VerifyCodeUseCase(repository, settings.CODE_MAX_FAIL_ATTEMPT_COUNT)


def get_success_verify_use_case(
    repository: IVerificationRepository = Depends(get_verification_code_reposirory),
    publisher: RabbitPublisher = Depends(get_auth_verify_publisher),
) -> SuccessVerifyUseCase:
    return SuccessVerifyUseCase(publisher, repository)
