from sqlalchemy.ext.asyncio import AsyncSession
from app.organizer.schemas import ProjectCreateIn
from app.organizer.use_cases.base_use_case import BaseProjectUseCase


class CreateProjectUseCase(BaseProjectUseCase):
    async def execute(
        self, session: AsyncSession, organizer_id: int, form: ProjectCreateIn
    ) -> int:
        async with session.begin():
            project = await self.project.create(
                session=session,
                name=form.name,
                description=form.description,
                start_time=form.start_time,
                organizer_id=organizer_id,
            )
            await self._create_or_update_roles(session, project.id, form.roles)
            await self.utils.create(project.id, project.start_time.replace(tzinfo=None))
            await session.commit()

            return project.id
