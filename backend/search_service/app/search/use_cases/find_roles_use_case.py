from core.interfaces.repositories.role import IRoleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import Role
from core.interfaces.use_case import IUseCase


class FindRolesUseCase(IUseCase):
    def __init__(self, repository: IRoleRepository) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, name_query: str | None, limit: int, offset: int
    ) -> list[Role]:
        if not name_query:
            return await self.repository.get(session, limit, offset)
        return await self.repository.find_by_name(session, name_query, limit, offset)
