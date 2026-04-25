from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    from core.models.postgres import async_session_maker

    async with async_session_maker() as session:
        yield session
