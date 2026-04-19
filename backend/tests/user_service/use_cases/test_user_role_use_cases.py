from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status

from user_service.app.user_role.use_cases.find_all_user_roles_use_case import (
    FindAllUserRoleUseCase,
)
from user_service.app.user_role.use_cases.find_user_role_by_id_use_case import (
    FindUserRoleByProjectIdUseCase,
)
from user_service.app.user_role.use_cases.add_or_update_user_role_use_case import (
    AddOrUpdateUserProjectApplicationUseCase,
)
from user_service.app.user_role.schemas import UserRoleIn


@pytest.mark.asyncio
async def test_find_all_user_roles_returns_projects_and_counts() -> None:
    p1 = SimpleNamespace(id=10)
    p2 = SimpleNamespace(id=20)
    repo = AsyncMock()
    repo.get_user_projects_with_roles = AsyncMock(return_value=[p1, p2])
    repo.get_user_forms_count = AsyncMock(return_value=[2, 1])

    use_case = FindAllUserRoleUseCase(repo)
    session = AsyncMock()

    projects, counts = await use_case.execute(session, user_id=4)

    assert projects == [p1, p2]
    assert counts == [2, 1]
    repo.get_user_forms_count.assert_awaited_once_with(
        session, [getattr(p1, "id", None), getattr(p2, "id", None)]
    )


@pytest.mark.asyncio
async def test_find_user_roles_by_project_delegates_to_repository() -> None:
    repo = AsyncMock()
    repo.get_user_roles_by_user_and_project = AsyncMock(
        return_value=[SimpleNamespace(user_id=1, project_role_id=10, priority=1)]
    )
    use_case = FindUserRoleByProjectIdUseCase(repo)
    session = AsyncMock()

    result = await use_case.execute(session, user_id=1, project_id=5)

    assert result[0].project_role_id == 10
    repo.get_user_roles_by_user_and_project.assert_awaited_once_with(session, 1, 5)


@pytest.mark.asyncio
async def test_add_or_update_user_roles_validates_and_persists() -> None:
    project = SimpleNamespace(
        id=1,
        status=SimpleNamespace(),
        roles=[SimpleNamespace(id=10), SimpleNamespace(id=11)],
    )
    project.status = "recruiting"
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=project)
    role_repo = AsyncMock()
    role_repo.delete_user_roles_for_user_and_project = AsyncMock()
    role_repo.create_user_roles_bulk = AsyncMock()

    use_case = AddOrUpdateUserProjectApplicationUseCase(role_repo, project_repo)
    session = AsyncMock()

    roles = [
        UserRoleIn(project_role_id=10, priority=1),
        UserRoleIn(project_role_id=11, priority=2),
    ]
    await use_case.execute(session, user_id=3, project_id=1, user_roles=roles)

    role_repo.delete_user_roles_for_user_and_project.assert_awaited_once_with(
        session, 3, 1
    )
    role_repo.create_user_roles_bulk.assert_awaited_once()
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_or_update_user_roles_raises_on_missing_project() -> None:
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=None)
    use_case = AddOrUpdateUserProjectApplicationUseCase(AsyncMock(), project_repo)
    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, user_id=1, project_id=99, user_roles=[])

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
