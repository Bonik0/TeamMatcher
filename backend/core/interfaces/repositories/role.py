from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import Role, UserProjectRole


class IRoleRepository(Protocol):
    async def get_by_names(self, session: AsyncSession, names: list[str]) -> list[Role]:
        pass

    async def get(self, session: AsyncSession, limit: int, offset: int) -> list[Role]:
        pass

    async def find_by_name(
        self, session: AsyncSession, name_query: str, limit: int, offset: int
    ) -> list[Role]:
        pass

    async def create_bulk(self, session: AsyncSession, names: list[str]) -> list[Role]:
        pass

    async def get_or_create_bulk(
        self, session: AsyncSession, names: list[str]
    ) -> dict[str, Role]:
        pass

    async def create_user_roles_bulk(
        self, session: AsyncSession, user_id: int, form: list[dict[str, int]]
    ) -> None:
        pass

    async def delete_user_roles_for_user_and_project(
        self, session: AsyncSession, user_id: int, project_id: int
    ) -> None:
        pass

    async def get_user_roles_by_user_and_project(
        self, session: AsyncSession, user_id: int, project_id: int
    ) -> list[UserProjectRole]:
        pass
