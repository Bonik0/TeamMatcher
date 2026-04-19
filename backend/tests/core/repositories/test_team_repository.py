from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.entities import ProjectStatus
from core.repositories.team import TeamRepository


def _result_with_scalars(*values: object) -> MagicMock:
    result = MagicMock()
    result.scalars.return_value.all.return_value = list(values)
    return result


@pytest.mark.asyncio
async def test_team_repository_create_bulk_skips_empty_payload() -> None:
    session = AsyncMock()
    repository = TeamRepository()

    assert await repository.create_bulk(session, []) is None
    session.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_team_repository_create_bulk_creates_teams_and_members() -> None:
    session = AsyncMock()
    session.execute.side_effect = [
        _result_with_scalars(SimpleNamespace(id=10), SimpleNamespace(id=11)),
        MagicMock(),
    ]
    repository = TeamRepository()

    await repository.create_bulk(
        session,
        teams_data=[
            {
                "name": "Team A",
                "project_id": 1,
                "members": [
                    {
                        "user_id": 100,
                        "project_role_id": 1000,
                        "role_score": 0.9,
                        "competence_match": 0.8,
                    }
                ],
            },
            {
                "name": "Team B",
                "project_id": 1,
                "members": [
                    {
                        "user_id": 101,
                        "project_role_id": 1001,
                        "role_score": 0.7,
                        "competence_match": 0.6,
                    }
                ],
            },
        ],
    )

    assert session.execute.await_count == 2


@pytest.mark.asyncio
async def test_team_repository_get_by_organizer_id_maps_projects() -> None:
    project_db = SimpleNamespace(id=1, organizer_id=7, status=ProjectStatus.COMPLETED)
    session = AsyncMock()
    session.execute.return_value = _result_with_scalars(project_db)
    repository = TeamRepository()

    with patch(
        "core.repositories.team.ProjectWithRolesAndTeams.model_validate",
        return_value="parsed-project",
    ) as model_validate:
        projects = await repository.get_by_organizer_id(session, organizer_id=7)

    assert projects == ["parsed-project"]
    model_validate.assert_called_once_with(project_db, from_attributes=True)


@pytest.mark.asyncio
async def test_team_repository_get_by_user_id_maps_teams() -> None:
    team_db = SimpleNamespace(id=1, name="Team A", project_id=3)
    session = AsyncMock()
    session.execute.return_value = _result_with_scalars(team_db)
    repository = TeamRepository()

    with patch(
        "core.repositories.team.TeamWithMembersAndProject.model_validate",
        return_value="parsed-team",
    ) as model_validate:
        teams = await repository.get_by_user_id(session, user_id=100)

    assert teams == ["parsed-team"]
    model_validate.assert_called_once_with(team_db, from_attributes=True)
