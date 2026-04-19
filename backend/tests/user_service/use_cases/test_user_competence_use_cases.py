from unittest.mock import AsyncMock
from types import SimpleNamespace

import pytest

from user_service.app.user_competence.use_cases.find_user_competence_use_case import (
    FindUserCompetencesUseCase,
)
from user_service.app.user_competence.use_cases.add_or_update_user_competence_use_case import (
    AddOrUpdateUserCompetencesUseCase,
)
from user_service.app.user_competence.use_cases.remove_user_competence_use_case import (
    RemoveUserCompetencesUseCase,
)
from user_service.app.user_competence.schemas import (
    AddOrUpdateUserCompetenceIn,
    UserCompetenceIn,
)
from fastapi import HTTPException, status


@pytest.mark.asyncio
async def test_find_user_competences_delegates_to_repository() -> None:
    repo = AsyncMock()
    repo.get_user_competences_by_user_id = AsyncMock(return_value=[SimpleNamespace()])
    use_case = FindUserCompetencesUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, user_id=3)

    assert result == [SimpleNamespace()]
    repo.get_user_competences_by_user_id.assert_awaited_once_with(session, 3)


@pytest.mark.asyncio
async def test_add_or_update_user_competences_raises_on_missing_competences() -> None:
    repo = AsyncMock()
    repo.get_existing_ids = AsyncMock(return_value=[1])  # requested will include 2
    use_case = AddOrUpdateUserCompetencesUseCase(repo)
    session = AsyncMock()
    form = AddOrUpdateUserCompetenceIn(
        competences=[
            UserCompetenceIn(competence_id=1, level=1),
            UserCompetenceIn(competence_id=2, level=2),
        ]
    )  # type: ignore

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, user_id=1, form=form)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_add_or_update_user_competences_calls_repository_and_commits() -> None:
    repo = AsyncMock()
    repo.get_existing_ids = AsyncMock(return_value=[1, 2])
    repo.add_or_update_user_competence_bulk = AsyncMock()
    use_case = AddOrUpdateUserCompetencesUseCase(repo)
    session = AsyncMock()
    form = AddOrUpdateUserCompetenceIn(
        competences=[
            UserCompetenceIn(competence_id=1, level=1),
            UserCompetenceIn(competence_id=2, level=2),
        ]
    )  # type: ignore

    await use_case.execute(session, user_id=5, form=form)

    repo.add_or_update_user_competence_bulk.assert_awaited_once_with(
        session, 5, [{"competence_id": 1, "level": 1}, {"competence_id": 2, "level": 2}]
    )
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_remove_user_competences_calls_repository_and_commits() -> None:
    repo = AsyncMock()
    repo.remove_user_competence_bulk = AsyncMock()
    use_case = RemoveUserCompetencesUseCase(repo)
    session = AsyncMock()

    await use_case.execute(session, user_id=7, competence_ids=[10, 11])

    repo.remove_user_competence_bulk.assert_awaited_once_with(session, 7, [10, 11])
    session.commit.assert_awaited_once()
