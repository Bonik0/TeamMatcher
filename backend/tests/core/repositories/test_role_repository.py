from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.entities import Role
from core.repositories.role import SQLAlchemyRoleRepository


def _roles_result(*roles: object) -> MagicMock:
    result = MagicMock()
    result.scalars.return_value.all.return_value = list(roles)
    return result


@pytest.mark.asyncio
async def test_role_repository_get_by_names_returns_empty_list_for_empty_input() -> (
    None
):
    session = AsyncMock()
    repository = SQLAlchemyRoleRepository()

    assert await repository.get_by_names(session, []) == []
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_role_repository_get_by_names_maps_roles() -> None:
    session = AsyncMock()
    session.execute.return_value = _roles_result(
        SimpleNamespace(id=1, name="Backend"),
        SimpleNamespace(id=2, name="Frontend"),
    )
    repository = SQLAlchemyRoleRepository()

    roles = await repository.get_by_names(session, ["Backend", "Frontend"])

    assert roles == [Role(id=1, name="Backend"), Role(id=2, name="Frontend")]


@pytest.mark.asyncio
async def test_role_repository_get_and_find_by_name_map_results() -> None:
    session = AsyncMock()
    session.execute.side_effect = [
        _roles_result(SimpleNamespace(id=1, name="Backend")),
        _roles_result(SimpleNamespace(id=2, name="Frontend")),
    ]
    repository = SQLAlchemyRoleRepository()

    roles = await repository.get(session, limit=10, offset=0)
    filtered_roles = await repository.find_by_name(session, "Front", limit=10, offset=0)

    assert roles == [Role(id=1, name="Backend")]
    assert filtered_roles == [Role(id=2, name="Frontend")]


@pytest.mark.asyncio
async def test_role_repository_create_bulk_maps_created_roles() -> None:
    session = AsyncMock()
    session.execute.return_value = _roles_result(SimpleNamespace(id=1, name="Backend"))
    repository = SQLAlchemyRoleRepository()

    roles = await repository.create_bulk(session, ["Backend", "Backend"])

    assert roles == [Role(id=1, name="Backend")]


@pytest.mark.asyncio
async def test_role_repository_get_or_create_bulk_returns_existing_and_created_roles() -> (
    None
):
    repository = SQLAlchemyRoleRepository()
    session = AsyncMock()
    existing_role = Role(id=1, name="Backend")
    created_role = Role(id=2, name="Frontend")

    with (
        patch.object(
            repository, "get_by_names", AsyncMock(return_value=[existing_role])
        ),
        patch.object(repository, "create_bulk", AsyncMock(return_value=[created_role])),
    ):
        roles = await repository.get_or_create_bulk(
            session,
            ["Backend", "Frontend", "Backend"],
        )

    assert roles == {
        "Backend": existing_role,
        "Frontend": created_role,
    }


@pytest.mark.asyncio
async def test_role_repository_get_or_create_bulk_returns_empty_dict_for_empty_input() -> (
    None
):
    repository = SQLAlchemyRoleRepository()

    assert await repository.get_or_create_bulk(AsyncMock(), []) == {}


@pytest.mark.asyncio
async def test_role_repository_create_user_roles_bulk_skips_empty_form() -> None:
    session = AsyncMock()
    repository = SQLAlchemyRoleRepository()

    assert await repository.create_user_roles_bulk(session, user_id=1, form=[]) is None
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_role_repository_create_user_roles_bulk_executes_insert() -> None:
    session = AsyncMock()
    repository = SQLAlchemyRoleRepository()

    await repository.create_user_roles_bulk(
        session,
        user_id=1,
        form=[
            {"project_role_id": 10, "priority": 1},
            {"project_role_id": 11, "priority": 2},
        ],
    )

    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_role_repository_deletes_user_roles_for_project() -> None:
    session = AsyncMock()
    repository = SQLAlchemyRoleRepository()

    await repository.delete_user_roles_for_user_and_project(
        session,
        user_id=7,
        project_id=3,
    )

    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_role_repository_get_user_roles_by_user_and_project_maps_entities() -> (
    None
):
    session = AsyncMock()
    session.execute.return_value = _roles_result(
        SimpleNamespace(user_id=1, project_role_id=10, priority=1),
        SimpleNamespace(user_id=1, project_role_id=11, priority=2),
    )
    repository = SQLAlchemyRoleRepository()

    roles = await repository.get_user_roles_by_user_and_project(
        session, user_id=1, project_id=5
    )

    assert [(role.project_role_id, role.priority) for role in roles] == [
        (10, 1),
        (11, 2),
    ]
