from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.entities import UserCompetenceLevelType, UserRoleType
from core.repositories.user import SQLAlchemyUserRepository


@pytest.mark.asyncio
async def test_user_repository_create_returns_created_id() -> None:
    result = MagicMock()
    result.scalar_one.return_value = 15
    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)
    repository = SQLAlchemyUserRepository()

    created_id = await repository.create(
        session=session,
        email="user@example.com",
        first_name="Ivan",
        patronymic=None,
        surname="Ivanov",
        role=UserRoleType.user,
        hashed_password="hash",
    )

    assert created_id == 15


@pytest.mark.asyncio
async def test_user_repository_get_by_email_returns_none_for_missing_user() -> None:
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)
    repository = SQLAlchemyUserRepository()

    assert await repository.get_by_email(session, "user@example.com") is None


@pytest.mark.asyncio
async def test_user_repository_get_by_email_maps_database_model() -> None:
    user_db = SimpleNamespace(
        id=1,
        email="user@example.com",
        first_name="Ivan",
        patronymic=None,
        surname="Ivanov",
        role=UserRoleType.user,
        hash_password="hash",
    )
    result = MagicMock()
    result.scalar_one_or_none.return_value = user_db
    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)
    repository = SQLAlchemyUserRepository()

    user = await repository.get_by_email(session, "user@example.com")

    assert user is not None
    assert user.id == 1
    assert user.email == "user@example.com"


@pytest.mark.asyncio
async def test_user_repository_update_password_returns_updated_user_id() -> None:
    result = MagicMock()
    result.scalar_one_or_none.return_value = 3
    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)
    repository = SQLAlchemyUserRepository()

    assert (
        await repository.update_password(session, "user@example.com", "new-hash") == 3
    )


@pytest.mark.asyncio
async def test_user_repository_get_with_priorities_and_competences_maps_users() -> None:
    user_db = SimpleNamespace(
        id=1,
        email="user@example.com",
        first_name="Ivan",
        patronymic=None,
        surname="Ivanov",
        role=UserRoleType.user,
        hash_password="hash",
        forms=[SimpleNamespace(user_id=1, project_role_id=11, priority=1)],
        competences=[
            SimpleNamespace(
                user_id=1,
                competence_id=7,
                level=UserCompetenceLevelType.HIGH,
            )
        ],
    )
    exec_result = MagicMock()
    exec_result.unique.return_value.scalars.return_value.all.return_value = [user_db]
    session = AsyncMock()
    session.execute = AsyncMock(return_value=exec_result)
    repository = SQLAlchemyUserRepository()

    users = await repository.get_with_priorities_and_competences(session, project_id=5)

    assert len(users) == 1
    assert users[0].forms[0].project_role_id == 11
    assert users[0].competences[0].competence_id == 7
