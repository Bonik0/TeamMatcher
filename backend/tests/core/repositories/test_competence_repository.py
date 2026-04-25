from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.entities import (
    Competence,
    UserCompetence,
    UserCompetenceLevelType,
    UserCompetenceWithCompetence,
)
from core.repositories.competence import SQLAlchemyCompetenceRepository


def _result_with_scalars(*values: object) -> MagicMock:
    result = MagicMock()
    result.scalars.return_value.all.return_value = list(values)
    return result


@pytest.mark.asyncio
async def test_competence_repository_short_circuits_empty_inputs() -> None:
    session = AsyncMock()
    repository = SQLAlchemyCompetenceRepository()

    assert await repository.get_by_names(session, []) == []
    assert await repository.get_existing_ids(session, []) == []
    assert await repository.get_or_create_bulk(session, []) == {}

    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_competence_repository_get_create_and_find_map_results() -> None:
    session = AsyncMock()
    session.execute.side_effect = [
        _result_with_scalars(SimpleNamespace(id=1, name="Python")),
        _result_with_scalars(SimpleNamespace(id=2, name="SQL")),
        _result_with_scalars(SimpleNamespace(id=3, name="Docker")),
        _result_with_scalars(1, 2),
    ]
    repository = SQLAlchemyCompetenceRepository()

    assert await repository.get_by_names(session, ["Python"]) == [
        Competence(id=1, name="Python")
    ]
    assert await repository.get(session, limit=10, offset=0) == [
        Competence(id=2, name="SQL")
    ]
    assert await repository.find_by_name(session, "Dock", limit=10, offset=0) == [
        Competence(id=3, name="Docker")
    ]
    assert await repository.get_existing_ids(session, [1, 2, 99]) == [1, 2]


@pytest.mark.asyncio
async def test_competence_repository_create_bulk_maps_created_competences() -> None:
    session = AsyncMock()
    session.execute.return_value = _result_with_scalars(
        SimpleNamespace(id=1, name="Python")
    )
    repository = SQLAlchemyCompetenceRepository()

    competences = await repository.create_bulk(session, ["Python", "Python"])

    assert competences == [Competence(id=1, name="Python")]


@pytest.mark.asyncio
async def test_competence_repository_get_or_create_bulk_merges_existing_and_new_items() -> (
    None
):
    repository = SQLAlchemyCompetenceRepository()
    session = AsyncMock()
    existing = Competence(id=1, name="Python")
    created = Competence(id=2, name="SQL")

    with (
        patch.object(repository, "get_by_names", AsyncMock(return_value=[existing])),
        patch.object(repository, "create_bulk", AsyncMock(return_value=[created])),
    ):
        competences = await repository.get_or_create_bulk(
            session,
            ["Python", "SQL", "Python"],
        )

    assert competences == {"Python": existing, "SQL": created}


@pytest.mark.asyncio
async def test_competence_repository_add_or_update_skips_empty_payload() -> None:
    session = AsyncMock()
    repository = SQLAlchemyCompetenceRepository()

    await repository.add_or_update_user_competence_bulk(
        session, user_id=1, competences=[]
    )

    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_competence_repository_add_or_update_executes_upsert() -> None:
    session = AsyncMock()
    repository = SQLAlchemyCompetenceRepository()

    await repository.add_or_update_user_competence_bulk(
        session,
        user_id=1,
        competences=[{"competence_id": 10, "level": UserCompetenceLevelType.HIGH}],
    )

    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_competence_repository_remove_user_competence_bulk_skips_empty_ids() -> (
    None
):
    session = AsyncMock()
    repository = SQLAlchemyCompetenceRepository()

    await repository.remove_user_competence_bulk(session, user_id=1, competence_ids=[])

    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_competence_repository_remove_user_competence_bulk_executes_delete() -> (
    None
):
    session = AsyncMock()
    repository = SQLAlchemyCompetenceRepository()

    await repository.remove_user_competence_bulk(
        session, user_id=1, competence_ids=[1, 2]
    )

    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_competence_repository_get_user_competences_by_user_id_maps_nested_competence() -> (
    None
):
    session = AsyncMock()
    session.execute.return_value = _result_with_scalars(
        SimpleNamespace(
            user_id=1,
            competence_id=10,
            level=UserCompetenceLevelType.HIGH,
            competence=SimpleNamespace(id=10, name="Python"),
        )
    )
    repository = SQLAlchemyCompetenceRepository()

    competences = await repository.get_user_competences_by_user_id(session, user_id=1)

    assert competences == [
        UserCompetenceWithCompetence(
            user_id=1,
            competence_id=10,
            level=UserCompetenceLevelType.HIGH,
            competence=Competence(id=10, name="Python"),
        )
    ]


@pytest.mark.asyncio
async def test_competence_repository_get_user_competence_by_user_ids_maps_entities() -> (
    None
):
    session = AsyncMock()
    session.execute.return_value = _result_with_scalars(
        SimpleNamespace(
            user_id=1, competence_id=10, level=UserCompetenceLevelType.MIDDLE
        )
    )
    repository = SQLAlchemyCompetenceRepository()

    competences = await repository.get_user_competence_by_user_ids(
        session, user_ids=[1, 2]
    )

    assert competences == [
        UserCompetence(
            user_id=1,
            competence_id=10,
            level=UserCompetenceLevelType.MIDDLE,
        )
    ]
