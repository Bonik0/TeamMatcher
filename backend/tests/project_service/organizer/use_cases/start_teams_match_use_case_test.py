from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from core.entities import ProjectStatus
from project_service.app.organizer.use_cases.start_teams_match_use_case import (
    StartTeamsMatchUseCase,
)


@pytest.mark.asyncio
async def test_start_match_raises_when_project_missing() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(return_value=None)
    use_case = StartTeamsMatchUseCase(repo, AsyncMock())
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=1, project_id=9)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_start_match_raises_when_wrong_status() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(
        return_value=SimpleNamespace(
            id=1,
            organizer_id=1,
            status=ProjectStatus.COMPLETED,
        )
    )
    use_case = StartTeamsMatchUseCase(repo, AsyncMock())
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=1, project_id=1)

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_start_match_raises_when_not_owner() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(
        return_value=SimpleNamespace(
            id=1,
            organizer_id=1,
            status=ProjectStatus.RECRUITING,
        )
    )
    use_case = StartTeamsMatchUseCase(repo, AsyncMock())
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=99, project_id=1)

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_start_match_calls_utils_update() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(
        return_value=SimpleNamespace(
            id=7,
            organizer_id=2,
            status=ProjectStatus.RECRUITING,
        )
    )
    utils = AsyncMock()
    use_case = StartTeamsMatchUseCase(repo, utils)
    session = AsyncMock()
    fixed_now = datetime(2026, 1, 1, 12, 0, 0)

    with patch(
        "project_service.app.organizer.use_cases.start_teams_match_use_case.datetime"
    ) as dt_mock:
        dt_mock.now.return_value = fixed_now

        await use_case.execute(session, organizer_id=2, project_id=7)

    utils.update.assert_awaited_once_with(7, fixed_now.replace(tzinfo=None))
