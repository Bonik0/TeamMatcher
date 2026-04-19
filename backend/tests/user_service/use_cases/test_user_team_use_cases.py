from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from user_service.app.user_team.use_cases.find_user_teams_use_case import (
    FindUserTeamsUseCase,
)


@pytest.mark.asyncio
async def test_find_user_teams_delegates_to_repository() -> None:
    repo = AsyncMock()
    repo.get_by_user_id = AsyncMock(return_value=[SimpleNamespace(id=1)])
    use_case = FindUserTeamsUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, user_id=9)

    assert result == [SimpleNamespace(id=1)]
    repo.get_by_user_id.assert_awaited_once_with(session, 9)
