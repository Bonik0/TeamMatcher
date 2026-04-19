from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from search_service.app.search.use_cases.find_project_use_case import FindProjectUseCase


@pytest.mark.asyncio
async def test_find_project_calls_repository_and_returns_projects_and_counts() -> None:
    project = SimpleNamespace(id=11)
    repo = AsyncMock()
    repo.get_by_roles_and_competences = AsyncMock(return_value=[project])
    repo.get_user_forms_count = AsyncMock(return_value=[5])

    use_case = FindProjectUseCase(repo)
    session = AsyncMock()

    projects, counts = await use_case.execute(
        session, "AI", [1], [2], limit=10, offset=0
    )

    assert projects == [project]
    assert counts == [5]
    repo.get_by_roles_and_competences.assert_awaited_once_with(
        session, "AI", [1], [2], 10, 0
    )
    repo.get_user_forms_count.assert_awaited_once_with(session, [11])
