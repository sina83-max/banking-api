from typing import AsyncGenerator

from backend.app.core.logging import get_logger

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.app.core.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger()

engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    except Exception as e:
        logger.error(f"database session error: {e}")
        if session:
            try:
                await session.rollback()
                logger.info(f"Successfully rolled back session after error")
            except Exception as rollback_error:
                logger.error(f"Error during session rollback: {rollback_error}")
        raise
    finally:
        if session:
            try:
                await session.close()
                logger.debug("Database session closed successfully")
            except Exception as close_error:
                logger.error(f"Error closing database session: {close_error}")

async def init_db() -> None:
    pass