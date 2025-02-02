from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncSession
)
from app.core.config import DB_URL
from typing import AsyncGenerator


engine = create_async_engine(DB_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
