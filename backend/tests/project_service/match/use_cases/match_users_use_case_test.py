from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.entities import (
    ProjectStatus,
    UserCompetence,
    UserCompetenceLevelType,
    UserProjectRole,
    UserProjectScore,
    UserRoleType,
    UserWithFormsAndCompetences,
)
from project_service.app.match.use_cases.match_users_use_case import MatchUsersUseCase


@pytest.mark.asyncio
async def test_match_users_logs_and_returns_when_project_missing() -> None:
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=None)
    user_repo = AsyncMock()
    user_repo.get_with_priorities_and_competences = AsyncMock(
        return_value=[
            UserWithFormsAndCompetences(
                id=1,
                email="a@a.com",
                first_name="A",
                surname="B",
                patronymic=None,
                role=UserRoleType.user,
                hash_password="h",
                forms=[],
                competences=[],
            )
        ]
    )
    team_repo = AsyncMock()
    match_utils = MagicMock()
    logger = MagicMock()

    use_case = MatchUsersUseCase(
        project_repo, user_repo, team_repo, match_utils, logger
    )
    session = AsyncMock()

    await use_case.execute(session, project_id=42)

    logger.info.assert_any_call("incorrect project_id: 42")
    project_repo.update_status.assert_not_awaited()
    match_utils.execute.assert_not_called()


@pytest.mark.asyncio
async def test_match_users_logs_and_returns_when_no_users() -> None:
    project = MagicMock()
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=project)
    user_repo = AsyncMock()
    user_repo.get_with_priorities_and_competences = AsyncMock(return_value=[])
    team_repo = AsyncMock()
    match_utils = MagicMock()
    logger = MagicMock()

    use_case = MatchUsersUseCase(
        project_repo, user_repo, team_repo, match_utils, logger
    )
    session = AsyncMock()

    await use_case.execute(session, project_id=1)

    logger.info.assert_any_call("No users data")
    project_repo.update_status.assert_awaited_once()


@pytest.mark.asyncio
async def test_match_users_formats_teams_and_persists() -> None:
    project = MagicMock()
    project.roles = []
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=project)
    user_repo = AsyncMock()
    user_repo.get_with_priorities_and_competences = AsyncMock(
        return_value=[
            UserWithFormsAndCompetences(
                id=1,
                email="a@a.com",
                first_name="A",
                surname="B",
                patronymic=None,
                role=UserRoleType.user,
                hash_password="h",
                forms=[UserProjectRole(user_id=1, project_role_id=22, priority=1)],
                competences=[
                    UserCompetence(
                        user_id=1,
                        competence_id=1,
                        level=UserCompetenceLevelType.HIGH,
                    )
                ],
            )
        ]
    )
    team_repo = AsyncMock()
    score = UserProjectScore(
        user_id=11,
        project_role_id=22,
        competence_match=Decimal("0.5"),
        role_score=Decimal("1.5"),
    )
    match_utils = MagicMock()
    match_utils.execute = MagicMock(return_value=[[score]])
    logger = MagicMock()

    use_case = MatchUsersUseCase(
        project_repo, user_repo, team_repo, match_utils, logger
    )
    session = AsyncMock()

    await use_case.execute(session, project_id=7)

    match_utils.execute.assert_called_once()
    project_repo.update_status.assert_any_call(session, 7, ProjectStatus.FORMATED)
    project_repo.update_status.assert_any_call(session, 7, ProjectStatus.COMPLETED)
    team_repo.create_bulk.assert_awaited_once()
    args = team_repo.create_bulk.await_args[0]
    assert args[1][0]["name"] == "Команда № 1"
    assert args[1][0]["project_id"] == 7
    assert args[1][0]["members"][0]["user_id"] == 11
    assert session.commit.await_count == 2
