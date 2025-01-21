import logging
from sqlalchemy import select
from app.database.crud_usuario import CRUD_Usuario


logger = logging.getLogger(__name__)


class CRUD_Produtor(CRUD_Usuario):
    """CRUD para o modelo Produtor."""

    def __init__(self, db):
        """Inicia a classe com as configurações do banco de dados."""
        super().__init__(db)

    async def handle_farm_in_producer(
        self,
        producer_model: object,
        farm_model: object,
        producer_id: int,
        farm_id: int,
        is_add: bool = True,
    ) -> dict:
        """Adiciona uma fazenda a um produtor."""
        result_producer = await self.db.execute(
            select(producer_model).where(producer_model.id == producer_id)
        )
        producer = result_producer.scalars().first()
        if not producer:
            raise ValueError(f"Produtor com ID {producer_id} não encontrado.")

        result_farm = await self.db.execute(
            select(farm_model).where(farm_model.id == farm_id)
        )
        farm = result_farm.scalars().first()
        if not farm:
            raise ValueError(f"Fazenda com ID {farm_id} não encontrada.")

        producer.fazenda.append(farm) if is_add else producer.fazenda.remove(farm)
        try:
            await self.db.commit()
            await self.db.refresh(producer)
            logger.info(f"Dados atualizados em {producer_model.__tablename__}")
        except Exception as e:
            logger.error(f"Dados atualizados em {producer_model.__tablename__}: {e}")
            raise e

        return self.producer_mapping(producer)

    def producer_mapping(self, data: object) -> dict:
        """Mapeia os dados do produtor."""
        return {
            "id": data.id,
            "nome": data.nome,
            "telefone": data.telefone,
            "cpf_cnpj": data.cpf_cnpj,
            "email": data.email,
            "ativo": data.ativo,
            "fazendas": [
                {
                    "id": farm.id,
                    "nome": farm.nome,
                    "cidade": farm.cidade,
                    "estado": farm.estado,
                    "area_total": farm.area_total,
                    "area_agricultavel": farm.area_agricultavel,
                    "area_vegetacao": farm.area_vegetacao,
                    "ativo": farm.ativo,
                }
                for farm in data.fazenda
            ],
        }
