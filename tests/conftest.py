import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.main import app
from app.db.models import Base
from app.db.session import get_db


# Тестовая БД (SQLite для простоты)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Создание асинхронного движка и сессии
engine = create_async_engine(DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


# Фикстура для создания таблиц и очистки после тестов
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Фикстура для подключения к БД
@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


# Переопределение зависимости на тестовую БД
@pytest.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as ac:
        yield ac
