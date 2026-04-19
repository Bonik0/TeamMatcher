from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from project_service.app.organizer.schemas import CompetenceIn, ProjectCreateIn, RoleIn
from project_service.app.organizer.use_cases.create_project_use_case import (
    CreateProjectUseCase,
)


@pytest.mark.asyncio
async def test_create_project_returns_project_id_and_schedules_format() -> None:
    start = datetime.now() + timedelta(days=1)
    project_row = MagicMock()
    project_row.id = 42
    project_row.start_time = start

    project_repo = AsyncMock()
    project_repo.create = AsyncMock(return_value=project_row)
    role_repo = AsyncMock()
    competence_repo = AsyncMock()
    utils = AsyncMock()

    begin_cm = MagicMock()
    begin_cm.__aenter__ = AsyncMock(return_value=None)
    begin_cm.__aexit__ = AsyncMock(return_value=None)
    session = MagicMock()
    session.begin.return_value = begin_cm
    session.commit = AsyncMock()

    form = ProjectCreateIn(
        name="Alpha",
        description=None,
        start_time=start,
        roles=[
            RoleIn(
                name="Backend",
                description="API",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Python", importance=5)],
            )
        ],
    )

    use_case = CreateProjectUseCase(project_repo, role_repo, competence_repo, utils)

    with patch.object(use_case, "_create_or_update_roles", new_callable=AsyncMock):
        project_id = await use_case.execute(session, organizer_id=7, form=form)

    assert project_id == 42
    project_repo.create.assert_awaited_once()
    utils.create.assert_awaited_once_with(42, start.replace(tzinfo=None))
    session.commit.assert_awaited_once()
