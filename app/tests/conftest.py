import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import DataBase, Base
from fastapi.testclient import TestClient
from app.main import app
from app.config import DATABASE_TEST

DataBase = DataBase(DATABASE_TEST)
get_db = DataBase.get_db

DATABASE_URL = f"postgresql+asyncpg://{DATABASE_TEST['user']}:{DATABASE_TEST['password']}@{DATABASE_TEST['host']}:{DATABASE_TEST['port']}/{DATABASE_TEST['database']}"  # noqa

@pytest_asyncio.fixture(scope="function")
async def get_db():
    """Conexão com o banco de dados para os testes."""
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
def client(get_db):
    """Cliente do banco de dados"""

    async def override_get_db():
        async for session in get_db:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
