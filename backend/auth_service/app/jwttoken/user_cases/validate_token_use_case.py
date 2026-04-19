from app.jwttoken.utils import JWTService
from core.interfaces.repositories.token_black_list import IBlacklistRepository
from fastapi import HTTPException, status
from uuid import UUID
from core.entities import JWTTokenType, JWTTokenPayload
from core.interfaces.use_case import IUseCase


class ValidateTokenUseCase(IUseCase):
    def __init__(
        self, jwt_service: JWTService, repository: IBlacklistRepository
    ) -> None:
        self.jwt_service = jwt_service
        self.repository = repository

    async def execute(
        self, token: str, token_type: JWTTokenType = JWTTokenType.ACCESS
    ) -> JWTTokenPayload:
        payload = self.jwt_service.decode_token(token)
        if payload.type != token_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid token type, expected {token_type}",
            )

        device_id = UUID(payload.device_id)
        user_id = payload.user_id
        iat = payload.iat

        is_device_blacklisted = await self.repository.is_device_blacklisted(device_id)

        if is_device_blacklisted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token has been revoked"
            )

        revoke_ts = await self.repository.get_user_revocation_timestamp(user_id)

        if revoke_ts is not None and iat.timestamp() < revoke_ts:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User tokens have been revoked",
            )

        return payload
