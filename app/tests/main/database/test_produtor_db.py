import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.models import Produtor, Fazenda
from app.tests.fixtures.produtor import producers_in_db
from app.tests.fixtures.fazenda import farms_in_db


@pytest.mark.asyncio
async def test_create_producer(get_db, farms_in_db):
    """Testa a criação de um novo produtor."""
    new_producer = Produtor(
        nome="Pedro da Silva",
        cpf_cnpj="93231382076",
        telefone="11985768364",
        email="pedro.silva@teste.com.br",
        senha="123Abc!!",
        tipo="comum",
        ativo=True,
    )

    farms = await get_db.execute(select(Fazenda))
    farms = farms.scalars().all()
    farms[0].produtor = new_producer
    farms[1].produtor = new_producer

    get_db.add(new_producer)
    await get_db.commit()
    await get_db.refresh(new_producer)

    # usuário foi salvo corretamenente
    assert new_producer.id is not None
    assert new_producer.nome == "Pedro da Silva"
    assert new_producer.email == "pedro.silva@teste.com.br"
    assert new_producer.tipo == "comum"
    assert new_producer.ativo is True
    assert new_producer.fazenda[0].nome == "Fazenda Primavera"
    assert new_producer.fazenda[1].nome == "Fazenda Sol Nascente"

    # usuário já existe
    duplicate_producer = Produtor(
        nome="Pedro da Silva",
        cpf_cnpj="93231382076",
        telefone="11985768364",
        email="pedro.silva@teste.com.br",
        senha="123Abc!!",
        tipo="comum",
        ativo=True,
    )
    get_db.add(duplicate_producer)
    with pytest.raises(IntegrityError):
        await get_db.commit()

    get_db.rollback()


@pytest.mark.asyncio
async def test_get_producers(get_db, producers_in_db):
    """Testa a obtenção de produtores."""
    result = await get_db.execute(select(Produtor))
    producers = result.scalars().all()
    # TODO: Verificar bug de criacao de 9 produtores ao invés de 9
    assert len(producers) > 0


@pytest.mark.asyncio
async def test_get_producer_by_name(get_db, producers_in_db):
    """Testa a obtenção de um produtor pelo nome."""
    result = await get_db.execute(select(Produtor).where(Produtor.nome == "Bruno Lima"))
    producer = result.scalars().first()
    assert producer is not None


@pytest.mark.asyncio
async def test_update_producer(get_db, producers_in_db):
    """Testa a atualização de um produtor."""
    result = await get_db.execute(select(Produtor).where(Produtor.nome == "Bruno Lima"))
    producer = result.scalars().first()
    producer.ativo = False
    await get_db.commit()
    result = await get_db.execute(select(Produtor).where(Produtor.nome == "Bruno Lima"))
    producer = result.scalars().first()
    assert producer.ativo is False


@pytest.mark.asyncio
async def test_delete_producer(get_db, producers_in_db, farms_in_db):
    """Testa a exclusão de um produtor."""
    result = await get_db.execute(select(Produtor).where(Produtor.nome == "Bruno Lima"))
    producer = result.scalars().first()
    await get_db.delete(producer)
    await get_db.commit()
    result = await get_db.execute(select(Produtor).where(Produtor.nome == "Bruno Lima"))
    producer = result.scalars().first()
    assert producer is None

    # produtor está associado a fazenda, a faszenda não deve ser excluida
    result_producer_with_farm = await get_db.execute(
        select(Produtor).where(Produtor.id == 2)
    )
    producer_with_farm = result_producer_with_farm.scalars().first()
    farms = await get_db.execute(select(Fazenda))
    farms = farms.scalars().all()
    expected_len = len(farms)
    farms[0].fazenda = producer_with_farm
    farms[1].fazenda = producer_with_farm
    await get_db.delete(producer_with_farm)
    await get_db.commit()
    farms = await get_db.execute(select(Fazenda))
    farms = farms.scalars().all()
    assert len(farms) == expected_len
