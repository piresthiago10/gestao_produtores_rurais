from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

class Base(DeclarativeBase):
    """Classe de base para o banco de dados."""
    pass

class DataBase:
    """Classe de conexão com o banco de dados."""

    def __init__(self, db_config = {}):
        """Inicia a classe com as configurações do banco de dados."""
        self.db_config = db_config
        self.host = self.db_config.get("host", "")
        self.user = self.db_config.get("user", "")
        self.password = self.db_config.get("password", "")
        self.db_name = self.db_config.get("database", "")
        self.check_same_thread = self.db_config.get("check_same_thread", "")
        self.connection = self.db_config.get("connection", "")
        self.autocommit = self.db_config.get("autocommit", "")
        self.autoflush = self.db_config.get("autoflush", "")
    
    def _create_engine(self) -> object:
        """Cria o engine de conexão com o banco de dados."""
        DATABASE_URL = "sqlite+aiosqlite:///./app.db"
        # DATABASE_URL = f"{self.connection}://{self.user}:{self.password}@{self.host}/{self.db_name}"

        engine = create_async_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": self.check_same_thread}
        )
        return engine

    def _create_session(self) -> sessionmaker:
        """Cria a sessão de conexão com o banco de dados."""
        engine = self._create_engine()
        return async_sessionmaker(autocommit=self.autocommit, autoflush=self.autoflush, bind=engine)

    async def get_db(self) -> object:
        """Retorna a sessão de conexão com o banco de dados."""
        async with self._create_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        session = self._create_session()
        try:
            yield session
        finally:
            session.close()