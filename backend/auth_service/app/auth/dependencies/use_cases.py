from fastapi import Depends
import logging
import os
from core.interfaces.repositories.user import IUserRepository
from core.interfaces.repositories.hashing import IHashingRepository
from core.interfaces.repositories.user_verification import IUserVerificationRepository
from core.dependencies.repositories.user import get_user_repository
from core.dependencies.repositories.hashing import get_hasing_repository
from core.dependencies.repositories.user_verification import get_verification_repository
from app.auth.use_cases.login_case import LoginUserUseCase
from app.auth.use_cases.change_password_case import ChangePasswordUseCase
from app.auth.use_cases.register_case import RegisterUserUseCase


def get_register_use_case(
    repository: IUserRepository = Depends(get_user_repository),
    hashing: IHashingRepository = Depends(get_hasing_repository),
    verification: IUserVerificationRepository = Depends(get_verification_repository),
) -> RegisterUserUseCase:
    need_verification = os.getenv("NT") != "TRUE"
    return RegisterUserUseCase(
        repository,
        hashing,
        verification,
        need_verification,
        logging.getLogger("Register"),
    )


def get_login_user_case(
    repository: IUserRepository = Depends(get_user_repository),
    hashing: IHashingRepository = Depends(get_hasing_repository),
) -> LoginUserUseCase:
    return LoginUserUseCase(repository, hashing)


def get_change_password_user_case(
    repository: IUserRepository = Depends(get_user_repository),
    hashing: IHashingRepository = Depends(get_hasing_repository),
    verification: IUserVerificationRepository = Depends(get_verification_repository),
) -> ChangePasswordUseCase:
    need_verification = os.getenv("NT") != "TRUE"
    return ChangePasswordUseCase(
        repository,
        hashing,
        verification,
        need_verification,
        logging.getLogger("ChangePassword"),
    )
