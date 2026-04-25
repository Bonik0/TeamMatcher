from unittest.mock import AsyncMock

import pytest

from search_service.app.search.use_cases.find_competence_use_case import (
    FindCompetenceUseCase,
)


@pytest.mark.asyncio
async def test_find_competence_calls_get_when_query_empty() -> None:
    repo = AsyncMock()
    repo.get = AsyncMock(return_value=["c1"])
    repo.find_by_name = AsyncMock()

    use_case = FindCompetenceUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, None, limit=5, offset=0)

    assert result == ["c1"]
    repo.get.assert_awaited_once_with(session, 5, 0)
    repo.find_by_name.assert_not_awaited()


@pytest.mark.asyncio
async def test_find_competence_calls_find_by_name_when_query_present() -> None:
    repo = AsyncMock()
    repo.get = AsyncMock()
    repo.find_by_name = AsyncMock(return_value=["comp-match"])

    use_case = FindCompetenceUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, "SQL", limit=2, offset=0)

    assert result == ["comp-match"]
    repo.find_by_name.assert_awaited_once_with(session, "SQL", 2, 0)
