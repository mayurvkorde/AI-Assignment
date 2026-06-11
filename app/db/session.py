from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
AsyncEngine,
AsyncSession,
async_sessionmaker,
create_async_engine
)
from app.config.config import config


async_db_engine: AsyncEngine = create_async_engine(
    config.RDS_ASYNC_URI,
    echo=False,
    pool_size=40,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_db_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

@asynccontextmanager
async def acquire_db_session() -> AsyncGenerator [AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async_acquire_db_session = acquire_db_session