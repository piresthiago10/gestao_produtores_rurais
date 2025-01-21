from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class Base(DeclarativeBase):
    """Classe de base para o banco de dados."""

    pass


class DataBase:
    """Classe de conexão com o banco de dados."""

    def __init__(self, db_config={}):
        """Inicia a classe com as configurações do banco de dados."""
        self.db_config = db_config
        self.host = self.db_config.get("host", "")
        self.port = self.db_config.get("port", "")
        self.user = self.db_config.get("user", "")
        self.password = self.db_config.get("password", "")
        self.db_name = self.db_config.get("database", "")
        self.connection = self.db_config.get("connection", "")
        self.autocommit = self.db_config.get("autocommit", "")
        self.autoflush = self.db_config.get("autoflush", "")

    def _create_engine(self) -> object:
        """Cria o engine de conexão com o banco de dados."""
        DATABASE_URL = f"{self.connection}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"  # noqa
        engine = create_async_engine(
            DATABASE_URL,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
        )
        return engine

    def _create_session(self) -> sessionmaker:
        """Cria a sessão de conexão com o banco de dados."""
        engine = self._create_engine()

        return sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_db(self) -> object:
        """Retorna a sessão de conexão com o banco de dados."""
        engine = self._create_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async_session = self._create_session()
        async with async_session() as session:
            yield session

        await engine.dispose()
