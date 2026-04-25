from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from project_service.app.organizer.use_cases.find_project_use_case import (
    FindProjectUseCase,
)


@pytest.mark.asyncio
async def test_find_project_returns_projects_and_form_counts() -> None:
    p1 = SimpleNamespace(id=10)
    p2 = SimpleNamespace(id=20)
    repo = AsyncMock()
    repo.get_by_organizer_id = AsyncMock(return_value=[p1, p2])
    repo.get_user_forms_count = AsyncMock(return_value=[3, 0])

    use_case = FindProjectUseCase(repo)
    session = AsyncMock()

    projects, counts = await use_case.execute(session, organizer_id=1)

    assert projects == [p1, p2]
    assert counts == [3, 0]
    repo.get_user_forms_count.assert_awaited_once_with(session, [10, 20])
