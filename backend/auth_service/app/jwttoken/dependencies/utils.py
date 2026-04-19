from app.jwttoken.utils import JWTGenerator, JWTService, AuthHeaderVerifyUtils
from fastapi import Depends
from app.jwttoken.config import get_jwt_token_settings, JWTTokenSettings


def get_jwt_token_generator() -> JWTGenerator:
    return JWTGenerator()


def get_jwt_token_service(
    settings: JWTTokenSettings = Depends(get_jwt_token_settings),
) -> JWTService:
    return JWTService(
        settings.SECRET,
        settings.ALGORITHM,
        settings.ACCESS_TOKEN_TTL.total_seconds(),
        settings.REFRESH_TOKEN_TTL.total_seconds(),
    )


def get_auth_header_verify() -> AuthHeaderVerifyUtils:
    return AuthHeaderVerifyUtils()
