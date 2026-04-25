from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status

from search_service.app.search.use_cases.find_project_by_id_use_case import (
    FindProjectByIdUseCase,
)


@pytest.mark.asyncio
async def test_find_project_by_id_raises_when_missing() -> None:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(return_value=None)
    use_case = FindProjectByIdUseCase(repo)
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, 99)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_find_project_by_id_returns_project_and_count() -> None:
    project = SimpleNamespace(id=7)
    repo = AsyncMock()
    repo.get_by_id = AsyncMock(return_value=project)
    repo.get_user_forms_count = AsyncMock(return_value=[2])

    use_case = FindProjectByIdUseCase(repo)
    session = AsyncMock()

    proj, count = await use_case.execute(session, 7)

    assert proj == project
    assert count == 2
    repo.get_user_forms_count.assert_awaited_once_with(session, [7])
