from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import Competence, UserCompetence, UserCompetenceWithCompetence


class ICompetenceRepository(Protocol):
    async def get_by_names(
        self, session: AsyncSession, names: list[str]
    ) -> list[Competence]:
        pass

    async def get(
        self, session: AsyncSession, limit: int, offset: int
    ) -> list[Competence]:
        pass

    async def find_by_name(
        self, session: AsyncSession, name_query: str, limit: int, offset: int
    ) -> list[Competence]:
        pass

    async def get_existing_ids(
        self, session: AsyncSession, competence_ids: list[int]
    ) -> list[int]:
        pass

    async def get_or_create_bulk(
        self, session: AsyncSession, names: list[str]
    ) -> dict[str, Competence]:
        pass

    async def create_bulk(
        self, session: AsyncSession, names: list[str]
    ) -> list[Competence]:
        pass

    async def add_or_update_user_competence_bulk(
        self, session: AsyncSession, user_id: int, competences: list[dict[str, int]]
    ) -> None:
        pass

    async def remove_user_competence_bulk(
        self, session: AsyncSession, user_id: int, competence_ids: list[int]
    ) -> None:
        pass

    async def get_user_competences_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> list[UserCompetenceWithCompetence]:
        pass

    async def get_user_competence_by_user_ids(
        self, session: AsyncSession, user_ids: list[int]
    ) -> list[UserCompetence]:
        pass
