from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.postgres import CompetenceDB, UserCompetenceAssociationDB
from core.interfaces.repositories.competence import ICompetenceRepository
from core.entities import Competence, UserCompetence, UserCompetenceWithCompetence
from sqlalchemy.dialects.postgresql import insert
from typing import Sequence


class SQLAlchemyCompetenceRepository(ICompetenceRepository):
    def _parse_competences(
        self, competences: Sequence[CompetenceDB]
    ) -> list[Competence]:
        return [
            Competence.model_validate(competence, from_attributes=True)
            for competence in competences
        ]

    async def get_by_names(
        self, session: AsyncSession, names: list[str]
    ) -> list[Competence]:
        if not names:
            return []
        result = await session.execute(
            select(CompetenceDB).where(CompetenceDB.name.in_(names))
        )
        return self._parse_competences(result.scalars().all())

    async def get(
        self, session: AsyncSession, limit: int, offset: int
    ) -> list[Competence]:
        query = (
            select(CompetenceDB).order_by(CompetenceDB.name).limit(limit).offset(offset)
        )
        result = await session.execute(query)
        return self._parse_competences(result.scalars().all())

    async def find_by_name(
        self, session: AsyncSession, name_query: str, limit: int, offset: int
    ) -> list[Competence]:
        query = (
            select(CompetenceDB)
            .where(CompetenceDB.name.like(f"%{name_query}%"))
            .order_by(CompetenceDB.name)
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        return self._parse_competences(result.scalars().all())

    async def get_existing_ids(
        self, session: AsyncSession, competence_ids: list[int]
    ) -> list[int]:
        if not competence_ids:
            return []
        query = select(CompetenceDB.id).where(CompetenceDB.id.in_(competence_ids))
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create_bulk(
        self, session: AsyncSession, names: list[str]
    ) -> list[Competence]:
        query = (
            insert(CompetenceDB)
            .on_conflict_do_nothing(index_elements=["id"])
            .returning(CompetenceDB)
            .values([{"name": name} for name in set(names)])
        )
        result = await session.execute(query)
        return self._parse_competences(result.scalars().all())

    async def get_or_create_bulk(
        self, session: AsyncSession, names: list[str]
    ) -> dict[str, Competence]:
        if not names:
            return {}

        names = list(set(names))

        existing_competence = await self.get_by_names(session, names)

        existing_names = [competence.name for competence in existing_competence]
        missing_names = [name for name in names if name not in existing_names]

        if missing_names:
            new_competences = await self.create_bulk(session, list(missing_names))
            existing_competence.extend(new_competences)

        return {competence.name: competence for competence in existing_competence}

    async def add_or_update_user_competence_bulk(
        self, session: AsyncSession, user_id: int, competences: list[dict[str, int]]
    ) -> None:
        if not competences:
            return
        query = insert(UserCompetenceAssociationDB).values(
            [{**competence, "user_id": user_id} for competence in competences]
        )
        query = query.on_conflict_do_update(
            index_elements=["user_id", "competence_id"],
            set_={"level": query.excluded.level},
        )
        await session.execute(query)

    async def remove_user_competence_bulk(
        self, session: AsyncSession, user_id: int, competence_ids: list[int]
    ) -> None:
        if not competence_ids:
            return
        query = delete(UserCompetenceAssociationDB).where(
            UserCompetenceAssociationDB.user_id == user_id,
            UserCompetenceAssociationDB.competence_id.in_(competence_ids),
        )
        await session.execute(query)

    async def get_user_competences_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> list[UserCompetenceWithCompetence]:
        query = (
            select(UserCompetenceAssociationDB)
            .options(selectinload(UserCompetenceAssociationDB.competence))
            .where(UserCompetenceAssociationDB.user_id == user_id)
        )
        result = await session.execute(query)
        return [
            UserCompetenceWithCompetence.model_validate(
                user_competence, from_attributes=True
            )
            for user_competence in result.scalars().all()
        ]

    async def get_user_competence_by_user_ids(
        self, session: AsyncSession, user_ids: list[int]
    ) -> list[UserCompetence]:
        query = select(UserCompetenceAssociationDB).where(
            UserCompetenceAssociationDB.user_id.in_(user_ids)
        )
        result = await session.execute(query)
        return [
            UserCompetence.model_validate(user_competence, from_attributes=True)
            for user_competence in result.scalars().all()
        ]
