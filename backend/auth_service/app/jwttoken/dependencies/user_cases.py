from app.jwttoken.user_cases.generate_token_case import GenerateTokensUseCase
from app.jwttoken.utils import JWTService
from fastapi import Depends
from app.jwttoken.dependencies.utils import get_jwt_token_service
from app.jwttoken.user_cases.validate_token_use_case import ValidateTokenUseCase
from core.dependencies.repositories.token_black_list import (
    get_token_blacklist_repository,
)
from core.interfaces.repositories.token_black_list import IBlacklistRepository
from app.jwttoken.user_cases.update_token_use_case import UpdateTokensUseCase
from app.jwttoken.user_cases.logout_use_case import LogoutUseCase
from app.jwttoken.user_cases.full_logout_use_case import FullLogoutUseCase


def get_generate_tokens_use_case(
    jwt_service: JWTService = Depends(get_jwt_token_service),
) -> GenerateTokensUseCase:
    return GenerateTokensUseCase(jwt_service)


def get_validate_token_use_case(
    jwt_service: JWTService = Depends(get_jwt_token_service),
    repository: IBlacklistRepository = Depends(get_token_blacklist_repository),
) -> ValidateTokenUseCase:
    return ValidateTokenUseCase(jwt_service, repository)


def get_update_tokens_use_case(
    repository: IBlacklistRepository = Depends(get_token_blacklist_repository),
    validate_token_use_case: ValidateTokenUseCase = Depends(
        get_validate_token_use_case
    ),
    generate_token_use_case: GenerateTokensUseCase = Depends(
        get_generate_tokens_use_case
    ),
) -> UpdateTokensUseCase:
    return UpdateTokensUseCase(
        repository, validate_token_use_case, generate_token_use_case
    )


def get_logout_use_case(
    repository: IBlacklistRepository = Depends(get_token_blacklist_repository),
    validate_token_use_case: ValidateTokenUseCase = Depends(
        get_validate_token_use_case
    ),
) -> LogoutUseCase:
    return LogoutUseCase(repository, validate_token_use_case)


def get_full_logout_use_case(
    jwt_service: JWTService = Depends(get_jwt_token_service),
    repository: IBlacklistRepository = Depends(get_token_blacklist_repository),
    validate_token_use_case: ValidateTokenUseCase = Depends(
        get_validate_token_use_case
    ),
) -> FullLogoutUseCase:
    return FullLogoutUseCase(jwt_service, repository, validate_token_use_case)
