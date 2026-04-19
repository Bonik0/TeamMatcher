from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    from core.models.postgres import async_session_maker

    return async_session_maker()
