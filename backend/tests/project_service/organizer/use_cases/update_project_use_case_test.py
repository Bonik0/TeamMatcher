from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from core.entities import ProjectStatus, Role
from project_service.app.organizer.schemas import CompetenceIn, ProjectUpdateIn, RoleIn
from project_service.app.organizer.use_cases.update_project_use_case import (
    UpdateProjectUseCase,
)


def _project_for_update() -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        organizer_id=10,
        status=ProjectStatus.RECRUITING,
        roles=[
            SimpleNamespace(
                role=Role(id=1, name="Backend"),
            ),
            SimpleNamespace(
                role=Role(id=2, name="Frontend"),
            ),
        ],
    )


@pytest.mark.asyncio
async def test_update_project_raises_when_project_missing() -> None:
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=None)
    use_case = UpdateProjectUseCase(project_repo, AsyncMock(), AsyncMock(), AsyncMock())
    session = AsyncMock()
    form = ProjectUpdateIn(
        project_id=1,
        name="X",
        description=None,
        start_time=datetime.now() + timedelta(days=1),
        roles=[
            RoleIn(
                name="Backend",
                description="d",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Py", importance=5)],
            )
        ],
    )

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=10, form=form)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_update_project_raises_when_not_recruiting() -> None:
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(
        return_value=SimpleNamespace(
            id=1,
            organizer_id=10,
            status=ProjectStatus.COMPLETED,
            roles=[],
        )
    )
    use_case = UpdateProjectUseCase(project_repo, AsyncMock(), AsyncMock(), AsyncMock())
    session = AsyncMock()
    form = ProjectUpdateIn(
        project_id=1,
        name="X",
        description=None,
        start_time=datetime.now() + timedelta(days=1),
        roles=[
            RoleIn(
                name="Backend",
                description="d",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Py", importance=5)],
            )
        ],
    )

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=10, form=form)

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_update_project_raises_when_wrong_organizer() -> None:
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=_project_for_update())
    use_case = UpdateProjectUseCase(project_repo, AsyncMock(), AsyncMock(), AsyncMock())
    session = AsyncMock()
    form = ProjectUpdateIn(
        project_id=1,
        name="X",
        description=None,
        start_time=datetime.now() + timedelta(days=1),
        roles=[
            RoleIn(
                name="Backend",
                description="d",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Py", importance=5)],
            ),
            RoleIn(
                name="Frontend",
                description="d",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Js", importance=5)],
            ),
        ],
    )

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=99, form=form)

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_update_project_raises_when_old_roles_removed() -> None:
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=_project_for_update())
    use_case = UpdateProjectUseCase(project_repo, AsyncMock(), AsyncMock(), AsyncMock())
    session = AsyncMock()
    form = ProjectUpdateIn(
        project_id=1,
        name="X",
        description=None,
        start_time=datetime.now() + timedelta(days=1),
        roles=[
            RoleIn(
                name="Backend",
                description="d",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Py", importance=5)],
            )
        ],
    )

    with pytest.raises(HTTPException) as exc:
        await use_case.execute(session, organizer_id=10, form=form)

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_update_project_commits_after_success() -> None:
    start = datetime.now() + timedelta(days=1)
    project_repo = AsyncMock()
    project_repo.get_by_id = AsyncMock(return_value=_project_for_update())
    project_repo.update = AsyncMock()
    utils = AsyncMock()
    session = AsyncMock()
    session.commit = AsyncMock()

    form = ProjectUpdateIn(
        project_id=1,
        name="New",
        description=None,
        start_time=start,
        roles=[
            RoleIn(
                name="Backend",
                description="d",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Py", importance=5)],
            ),
            RoleIn(
                name="Frontend",
                description="d",
                quantity_per_team=1,
                competences=[CompetenceIn(name="Js", importance=5)],
            ),
        ],
    )

    use_case = UpdateProjectUseCase(project_repo, AsyncMock(), AsyncMock(), utils)

    with patch.object(use_case, "_create_or_update_roles", new_callable=AsyncMock):
        await use_case.execute(session, organizer_id=10, form=form)

    project_repo.update.assert_awaited_once()
    utils.update.assert_awaited_once_with(1, start.replace(tzinfo=None))
    session.commit.assert_awaited_once()
