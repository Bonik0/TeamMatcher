from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.entities import ProjectRole, ProjectRoleCompetence, ProjectStatus
from core.repositories.project import SQLAlchemyProjectRepository


def _result_with_scalars(*values: object) -> MagicMock:
    result = MagicMock()
    result.scalars.return_value.all.return_value = list(values)
    return result


@pytest.mark.asyncio
async def test_project_repository_create_returns_parsed_project_and_strips_timezone() -> (
    None
):
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    project_db = SimpleNamespace(id=1)
    exec_result = MagicMock()
    exec_result.scalar_one.return_value = project_db
    session.execute = AsyncMock(return_value=exec_result)
    start_time = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    with patch.object(
        repository, "_parse_project", return_value="parsed-project"
    ) as parse_mock:
        project = await repository.create(
            session,
            organizer_id=7,
            name="Launch",
            description="Desc",
            start_time=start_time,
        )

    assert project == "parsed-project"
    parse_mock.assert_called_once_with(project_db)
    query = session.execute.await_args.args[0]
    assert query.compile().params["start_time"] == start_time.replace(tzinfo=None)


@pytest.mark.asyncio
async def test_project_repository_update_strips_timezone_and_executes_query() -> None:
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    start_time = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    await repository.update(
        session,
        project_id=9,
        name="Updated",
        description=None,
        start_time=start_time,
    )

    query = session.execute.await_args.args[0]
    assert query.compile().params["start_time"] == start_time.replace(tzinfo=None)


@pytest.mark.asyncio
async def test_project_repository_update_status_executes_query() -> None:
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()

    await repository.update_status(
        session, project_id=3, status=ProjectStatus.COMPLETED
    )

    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_project_repository_get_by_id_returns_none_for_missing_project() -> None:
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    exec_result = MagicMock()
    exec_result.scalar_one_or_none.return_value = None
    session.execute = AsyncMock(return_value=exec_result)

    assert await repository.get_by_id(session, project_id=1) is None


@pytest.mark.asyncio
async def test_project_repository_get_by_id_maps_project() -> None:
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    project_db = SimpleNamespace(id=1)
    exec_result = MagicMock()
    exec_result.scalar_one_or_none.return_value = project_db
    session.execute = AsyncMock(return_value=exec_result)

    with patch.object(
        repository,
        "_parse_project_with_roles_and_competences",
        return_value="parsed-project",
    ) as parse_mock:
        project = await repository.get_by_id(session, project_id=1)

    assert project == "parsed-project"
    parse_mock.assert_called_once_with(project_db)


@pytest.mark.asyncio
async def test_project_repository_get_by_organizer_id_maps_projects() -> None:
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    session.execute = AsyncMock(
        return_value=_result_with_scalars(SimpleNamespace(id=1), SimpleNamespace(id=2))
    )

    with patch.object(
        repository,
        "_parse_projects_with_roles_and_competences",
        return_value=["project-1", "project-2"],
    ) as parse_mock:
        projects = await repository.get_by_organizer_id(session, organizer_id=7)

    assert projects == ["project-1", "project-2"]
    parse_mock.assert_called_once()


@pytest.mark.asyncio
async def test_project_repository_get_by_roles_and_competences_applies_filters_and_maps_projects() -> (
    None
):
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    session.execute = AsyncMock(
        return_value=_result_with_scalars(SimpleNamespace(id=1))
    )

    with patch.object(
        repository,
        "_parse_projects_with_roles_and_competences",
        return_value=["project-1"],
    ) as parse_mock:
        projects = await repository.get_by_roles_and_competences(
            session,
            search_vector_value="AI",
            role_ids=[1, 2],
            competence_ids=[10, 11],
            limit=5,
            offset=2,
        )

    assert projects == ["project-1"]
    parse_mock.assert_called_once()
    query = session.execute.await_args.args[0]
    compiled_sql = str(query)
    assert "projects.name" in compiled_sql
    assert "role_id" in compiled_sql
    assert "competence_id" in compiled_sql


@pytest.mark.asyncio
async def test_project_repository_get_user_projects_with_roles_returns_unique_projects() -> (
    None
):
    repository = SQLAlchemyProjectRepository()
    result = MagicMock()
    result.scalars.return_value.unique.return_value.all.return_value = [
        SimpleNamespace(id=1)
    ]
    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)

    with patch.object(
        repository,
        "_parse_project_with_roles_and_forms",
        return_value=["project-1"],
    ) as parse_mock:
        projects = await repository.get_user_projects_with_roles(session, user_id=15)

    assert projects == ["project-1"]
    parse_mock.assert_called_once_with([SimpleNamespace(id=1)])


@pytest.mark.asyncio
async def test_project_repository_get_user_forms_count_preserves_requested_order() -> (
    None
):
    repository = SQLAlchemyProjectRepository()
    result = MagicMock()
    result.all.return_value = [(2, 7), (5, 3)]
    session = AsyncMock()
    session.execute = AsyncMock(return_value=result)

    counts = await repository.get_user_forms_count(session, project_ids=[5, 1, 2])

    assert counts == [3, 0, 7]


@pytest.mark.asyncio
async def test_project_repository_create_or_update_role_associations_returns_empty_dict_for_empty_input() -> (
    None
):
    repository = SQLAlchemyProjectRepository()

    assert (
        await repository.create_or_update_role_associations(
            AsyncMock(), project_id=1, project_roles=[]
        )
        == {}
    )


@pytest.mark.asyncio
async def test_project_repository_create_or_update_role_associations_maps_by_role_id() -> (
    None
):
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    raw_role = SimpleNamespace(role_id=10)
    session.execute = AsyncMock(return_value=_result_with_scalars(raw_role))

    with patch.object(
        repository,
        "_parse_project_role",
        return_value=ProjectRole(
            id=1,
            project_id=1,
            role_id=10,
            description="Lead",
            quantity_per_team=1,
        ),
    ):
        roles = await repository.create_or_update_role_associations(
            session,
            project_id=1,
            project_roles=[
                {
                    "role_id": 10,
                    "description": "Lead",
                    "quantity_per_team": 1,
                }
            ],
        )

    assert list(roles.keys()) == [10]
    assert roles[10].description == "Lead"


@pytest.mark.asyncio
async def test_project_repository_create_or_update_role_competence_associations_handles_empty_input() -> (
    None
):
    repository = SQLAlchemyProjectRepository()

    assert (
        await repository.create_or_update_role_competence_associations(
            AsyncMock(),
            role_competencies=[],
        )
        == []
    )


@pytest.mark.asyncio
async def test_project_repository_create_or_update_role_competence_associations_maps_items() -> (
    None
):
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()
    session.execute = AsyncMock(
        return_value=_result_with_scalars(SimpleNamespace(project_role_id=1))
    )

    with patch.object(
        repository,
        "_parse_project_role_competence",
        return_value=ProjectRoleCompetence(
            project_role_id=1,
            competence_id=7,
            importance=5,
        ),
    ) as parse_mock:
        competences = await repository.create_or_update_role_competence_associations(
            session,
            role_competencies=[
                {
                    "project_role_id": 1,
                    "competence_id": 7,
                    "importance": 5,
                }
            ],
        )

    assert competences == [
        ProjectRoleCompetence(project_role_id=1, competence_id=7, importance=5)
    ]
    parse_mock.assert_called_once()


@pytest.mark.asyncio
async def test_project_repository_deletes_role_competence_associations() -> None:
    repository = SQLAlchemyProjectRepository()
    session = AsyncMock()

    await repository.delete_role_competence_associations(
        session, project_role_ids=[1, 2, 3]
    )

    session.execute.assert_awaited_once()
