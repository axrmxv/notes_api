from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncSession
)
from sqlalchemy.future import select
from app.core.config import DB_URL
from app.db.models import Base, User

from passlib.context import CryptContext

from typing import AsyncGenerator


engine = create_async_engine(DB_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Инициализация базы данных: создание таблиц, если их нет
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Проверка наличия администратора
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.username == "admin")
        )
        admin = result.scalars().first()

        if not admin:
            hashed_password = pwd_context.hash("adminpass")
            new_admin = User(
                username="admin", password=hashed_password, role="admin"
            )
            session.add(new_admin)
            await session.commit()
            print("Администратор успешно создан.")
        else:
            print("Администратор уже существует.")
