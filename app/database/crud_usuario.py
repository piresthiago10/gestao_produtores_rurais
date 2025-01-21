import logging
from sqlalchemy import select
from app.database.crud import CRUD


logger = logging.getLogger(__name__)


class CRUD_Usuario(CRUD):
    """CRUD para o modelo Usuario."""

    def __init__(self, db):
        """Inicia a classe com as configurações do banco de dados."""
        super().__init__(db)

    async def get_by_cpf_cnpj(self, model, cpf_cnpj: str):
        """Retorna um usuário pelo cpf_cnpj."""
        try:
            result = await self.db.execute(
                select(model).where(model.cpf_cnpj == cpf_cnpj)
            )
            logger.info(f"Dados buscados em {model.__tablename__}")
        except Exception as e:
            logger.error(f"Dados buscados em {model.__tablename__}: {e}")
            raise e
        return result.scalars().first()

    async def get_by_email(self, model, email: int):
        """Retorna um usuário pelo email."""
        try:
            result = await self.db.execute(select(model).where(model.email == email))
            logger.info(f"Dados buscados em {model.__tablename__}")
        except Exception as e:
            logger.error(f"Dados buscados em {model.__tablename__}: {e}")
            raise e
        return result.scalars().first()
