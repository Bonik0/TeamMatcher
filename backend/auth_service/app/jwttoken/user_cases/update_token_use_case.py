from core.interfaces.repositories.token_black_list import IBlacklistRepository
from app.jwttoken.user_cases.validate_token_use_case import ValidateTokenUseCase
from core.entities import JWTTokenType
from uuid import UUID
from datetime import datetime
from app.jwttoken.user_cases.generate_token_case import GenerateTokensUseCase
from core.interfaces.use_case import IUseCase


class UpdateTokensUseCase(IUseCase):
    def __init__(
        self,
        repository: IBlacklistRepository,
        validate_token_use_case: ValidateTokenUseCase,
        generate_token_use_case: GenerateTokensUseCase,
    ) -> None:
        self.repository = repository
        self.validate_token_use_case = validate_token_use_case
        self.generate_token_use_case = generate_token_use_case

    async def execute(self, refresh_token: str, new_device_id: UUID) -> tuple[str, str]:
        payload = await self.validate_token_use_case.execute(
            refresh_token, JWTTokenType.REFRESH
        )

        user_id = payload.user_id
        role = payload.role
        device_id = UUID(payload.device_id)
        block_ttl = int(payload.exp.timestamp() - datetime.now().timestamp())

        await self.repository.add_device_to_blacklist(device_id, block_ttl)
        return await self.generate_token_use_case.execute(user_id, role, new_device_id)
