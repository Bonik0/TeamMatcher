from fastapi import Depends
from app.user_verify.use_cases.delete_case import DeleteUserVerificationUseCase
from app.user_verify.use_cases.save_case import SaveUserVerificationUseCase
from core.dependencies.repositories.user_verification import get_verification_repository
from core.interfaces.repositories.user_verification import IUserVerificationRepository
from app.user_verify.config import get_verification_settings, VerificationSettings
from app.user_verify.use_cases.find_case import FindUserVerificationUseCase


def get_save_use_case(
    repository: IUserVerificationRepository = Depends(get_verification_repository),
    settings: VerificationSettings = Depends(get_verification_settings),
) -> SaveUserVerificationUseCase:
    return SaveUserVerificationUseCase(repository, settings.LIFETIME)


def get_delete_use_case(
    repository: IUserVerificationRepository = Depends(get_verification_repository),
) -> DeleteUserVerificationUseCase:
    return DeleteUserVerificationUseCase(repository)


def get_find_use_case(
    repository: IUserVerificationRepository = Depends(get_verification_repository),
) -> FindUserVerificationUseCase:
    return FindUserVerificationUseCase(repository)
