import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Fazenda


@pytest_asyncio.fixture(scope="function")
async def farms_in_db(get_db: AsyncSession):
    """Fixture para criar três fazendas no banco de dados para os testes."""
    farms = [
        Fazenda(
            nome="Fazenda Primavera",
            cidade="Ribeirão Preto",
            estado="SP",
            area_total=500,
            area_agricultavel=300,
            area_vegetacao=200,
            ativo=True,
        ),
        Fazenda(
            nome="Fazenda Sol Nascente",
            cidade="São José do Rio Preto",
            estado="SP",
            area_total=750,
            area_agricultavel=500,
            area_vegetacao=250,
            ativo=True,
        ),
        Fazenda(
            nome="Fazenda Horizonte",
            cidade="Uberlândia",
            estado="MG",
            area_total=1000,
            area_agricultavel=700,
            area_vegetacao=300,
            ativo=False,
        ),
    ]

    async with get_db.begin():
        get_db.add_all(farms)
    await get_db.commit()

    return farms
