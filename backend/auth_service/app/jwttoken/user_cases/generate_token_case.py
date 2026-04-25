from uuid import UUID
from app.jwttoken.utils import JWTService
from core.entities import UserRoleType
from core.interfaces.use_case import IUseCase


class GenerateTokensUseCase(IUseCase):
    def __init__(self, jwt_service: JWTService) -> None:
        self.jwt_service = jwt_service

    async def execute(
        self, user_id: int, role: UserRoleType, device_id: UUID
    ) -> tuple[str, str]:
        return (
            self.jwt_service.create_access_token(user_id, role, device_id),
            self.jwt_service.create_refresh_token(user_id, role, device_id),
        )
