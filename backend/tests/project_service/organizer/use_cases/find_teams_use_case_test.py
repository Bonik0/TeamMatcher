from unittest.mock import AsyncMock

import pytest

from project_service.app.organizer.use_cases.find_teams_use_case import FindTeamsUseCase


@pytest.mark.asyncio
async def test_find_teams_delegates_to_repository() -> None:
    teams = [object()]
    repo = AsyncMock()
    repo.get_by_organizer_id = AsyncMock(return_value=teams)

    use_case = FindTeamsUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, organizer_id=3)

    assert result is teams
    repo.get_by_organizer_id.assert_awaited_once_with(session, 3)
