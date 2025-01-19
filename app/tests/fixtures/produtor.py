import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Produtor

@pytest_asyncio.fixture(scope="function")
async def producers_in_db(get_db: AsyncSession):
    """Fixture para criar três produtores no banco de dados para os testes."""
    producers = [
        Produtor(
            nome="Bruno Lima",
            cpf_cnpj="11223344556",
            telefone="11988776655",
            email="bruno.lima@teste.com.br",
            senha="Bruno123!",
            tipo="admin",
            ativo=True
        ),
        Produtor(
            nome="Laura Pereira",
            cpf_cnpj="22334455666",
            telefone="11922334455",
            email="laura.pereira@teste.com.br",
            senha="Laura456!",
            tipo="comum",
            ativo=False
        ),
        Produtor(
            nome="Gustavo Martins",
            cpf_cnpj="33445566777",
            telefone="11955667788",
            email="gustavo.martins@teste.com.br",
            senha="Gustavo789!",
            tipo="comum",
            ativo=True
        )
    ]
    async with get_db.begin():
        get_db.add_all(producers)
    await get_db.commit()

    return producers
