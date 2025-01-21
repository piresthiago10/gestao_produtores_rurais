import logging
from sqlalchemy import func, select
from app.database.crud import CRUD


logger = logging.getLogger(__name__)


class CRUD_Fazenda(CRUD):
    """CRUD para o modelo Fazenda."""

    def __init__(self, db):
        """Inicia a classe com as configurações do banco de dados."""
        super().__init__(db)

    async def get_total_farms(self, model):
        """Retorna o total de fazendas cadastradas."""
        result = await self.db.execute(select(func.count()).select_from(model))
        logger.info(f"Dados buscados em {model.__tablename__}")
        return result.scalars().all()[0]

    async def get_total_area(self, model):
        """Retorna o total de hectares registrados."""
        result = await self.db.execute(select(func.sum(model.area_total)))
        logger.info(f"Dados buscados em {model.__tablename__}")
        return result.scalars().all()[0]

    async def get_farms_by_state(self, model):
        """Retorna o total de fazendas por estado."""
        result = await self.db.execute(
            select(model.estado, func.count()).group_by(model.estado)
        )
        logger.info(f"Dados buscados em {model.__tablename__}")
        return [{"state": state, "total_farms": count} for state, count in result.all()]

    async def get_farms_by_culture(self, farm_model, crop_model):
        """Retorna o total de fazendas por cultura plantada."""
        result = await self.db.execute(
            select(
                crop_model.tipo_cultura, func.count(farm_model.id).label("total_farms")
            )
            .join(crop_model, crop_model.fazenda_id == farm_model.id)
            .group_by(crop_model.tipo_cultura)
        )
        data_list = []
        for tipo_cultura, total_farms in result.fetchall():
            data_list.append({"tipo_cultura": tipo_cultura, "total_farms": total_farms})
        logger.info(f"Dados buscados em {farm_model.__tablename__}")
        return data_list

    async def get_farms_by_soil_use(self, model):
        """Retorna o total de fazendas por uso do solo (área agricultável e vegetação)."""
        result = await self.db.execute(
            select(
                model.area_agricultavel,
                model.area_vegetacao,
                func.count().label("total_farms"),
            ).group_by(model.area_agricultavel, model.area_vegetacao)
        )
        data_list = []
        for area_agricultavel, area_vegetacao, total_farms in result.fetchall():
            data_list.append(
                {
                    "area_agricultavel": area_agricultavel,
                    "area_vegetacao": area_vegetacao,
                    "total_farms": total_farms,
                }
            )
        logger.info(f"Dados buscados em {model.__tablename__}")
        return data_list

    async def handle_crop_in_farm(
        self,
        farm_model: object,
        crop_model: object,
        farm_id: int,
        crop_id: int,
        is_add: bool = True,
    ) -> dict:
        """Adiciona uma fazenda a um produtor."""
        result_farm = await self.db.execute(
            select(farm_model).where(farm_model.id == farm_id)
        )
        farm = result_farm.scalars().first()
        if not farm:
            raise ValueError(f"Fazenda com ID {farm_id} não encontrada.")

        result_crop = await self.db.execute(
            select(crop_model).where(crop_model.id == crop_id)
        )
        crop = result_crop.scalars().first()
        if not crop:
            raise ValueError(f"Safra com ID {crop_id} não encontrada.")

        farm.safra.append(crop) if is_add else farm.safra.remove(crop)
        await self.db.commit()
        await self.db.refresh(farm)
        logger.info(f"Dados atualizados em {farm_model.__tablename__}")
        return self.farm_mapping(farm)

    def farm_mapping(self, data: object) -> dict:
        """Mapeia os dados da fazenda."""
        return {
            "id": data.id,
            "nome": data.nome,
            "cidade": data.cidade,
            "estado": data.estado,
            "area_total": data.area_total,
            "area_agricultavel": data.area_agricultavel,
            "area_vegetacao": data.area_vegetacao,
            "ativo": data.ativo,
            "safras": [
                {
                    "id": crop.id,
                    "nome": crop.nome,
                    "variedade": crop.variedade,
                    "tipo_cultura": crop.tipo_cultura,
                    "ano_colheita": crop.ano_colheita,
                    "produtividade_tonelada": crop.produtividade_tonelada,
                    "ativo": crop.ativo,
                }
                for crop in data.safra
            ],
        }
