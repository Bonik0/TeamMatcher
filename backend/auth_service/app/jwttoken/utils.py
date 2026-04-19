import jwt
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from core.entities import JWTTokenPayload, JWTTokenType, UserRoleType
from pydantic import ValidationError


class JWTService:
    def __init__(
        self, secret_key: str, algorithm: str, access_ttl_sec: int, refresh_ttl_sec: int
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_ttl_sec = access_ttl_sec
        self.refresh_ttl_sec = refresh_ttl_sec

    def _generate_token(
        self, user_id: int, device_id: UUID, ttl: int, type: str, role: UserRoleType
    ) -> str:
        now = datetime.now()
        payload = JWTTokenPayload(
            jti=str(uuid4()),
            user_id=user_id,
            role=role,
            device_id=str(device_id),
            type=type,
            exp=now + timedelta(seconds=ttl),
            iat=now,
        )
        return jwt.encode(
            payload.model_dump(), self.secret_key, algorithm=self.algorithm
        )

    def create_access_token(
        self, user_id: int, role: UserRoleType, device_id: UUID
    ) -> str:
        return self._generate_token(
            user_id, device_id, self.access_ttl_sec, JWTTokenType.ACCESS, role
        )

    def create_refresh_token(
        self, user_id: str, role: UserRoleType, device_id: UUID
    ) -> str:
        return self._generate_token(
            user_id, device_id, self.refresh_ttl_sec, JWTTokenType.REFRESH, role
        )

    def decode_token(self, token: str) -> JWTTokenPayload:
        try:
            return JWTTokenPayload.model_validate(
                jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        except (jwt.InvalidTokenError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )


class JWTGenerator:
    @staticmethod
    def get_device_id() -> UUID:
        return uuid4()


class AuthHeaderVerifyUtils:
    def verify(self, authorization_header: str | None) -> str:
        if authorization_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Need bearer token"
            )

        if "Bearer " not in authorization_header:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Header must include Bearer",
            )
        return authorization_header.removeprefix("Bearer ")
