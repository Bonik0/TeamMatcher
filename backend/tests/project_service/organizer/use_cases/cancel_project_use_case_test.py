from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from core.entities import ProjectStatus
from project_service.app.organizer.use_cases.cancel_project_use_case import (
    CancelProjectUseCase,
)


def _project() -> SimpleNamespace:
    return SimpleNamespace(
        id=5,
        organizer_id=2,
        status=ProjectStatus.RECRUITING,
    )


@pytest.mark.asyncio
async def test_cancel_project_raises_when_not_found() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(return_value=None)
    use_case = CancelProjectUseCase(repo, AsyncMock())
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=2, project_id=5)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_cancel_project_raises_when_not_recruiting() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(
        return_value=SimpleNamespace(
            id=5, organizer_id=2, status=ProjectStatus.COMPLETED
        )
    )
    use_case = CancelProjectUseCase(repo, AsyncMock())
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=2, project_id=5)

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_cancel_project_raises_when_not_owner() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(return_value=_project())
    use_case = CancelProjectUseCase(repo, AsyncMock())
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=99, project_id=5)

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_cancel_project_updates_status_and_utils() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(return_value=_project())
    repo.update_status = AsyncMock()
    utils = AsyncMock()
    session = AsyncMock()
    session.commit = AsyncMock()

    use_case = CancelProjectUseCase(repo, utils)

    await use_case.execute(session, organizer_id=2, project_id=5)

    repo.update_status.assert_awaited_once_with(session, 5, ProjectStatus.CANCELLED)
    utils.cancel.assert_awaited_once_with(5)
    session.commit.assert_awaited_once()
