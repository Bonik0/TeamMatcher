from unittest.mock import AsyncMock

import pytest

from search_service.app.search.use_cases.find_roles_use_case import FindRolesUseCase


@pytest.mark.asyncio
async def test_find_roles_calls_get_when_query_empty() -> None:
    repo = AsyncMock()
    repo.get = AsyncMock(return_value=["r1"])
    repo.find_by_name = AsyncMock()

    use_case = FindRolesUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, None, limit=5, offset=0)

    assert result == ["r1"]
    repo.get.assert_awaited_once_with(session, 5, 0)
    repo.find_by_name.assert_not_awaited()


@pytest.mark.asyncio
async def test_find_roles_calls_find_by_name_when_query_present() -> None:
    repo = AsyncMock()
    repo.get = AsyncMock()
    repo.find_by_name = AsyncMock(return_value=["role-match"])

    use_case = FindRolesUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, "Back", limit=3, offset=1)

    assert result == ["role-match"]
    repo.find_by_name.assert_awaited_once_with(session, "Back", 3, 1)
