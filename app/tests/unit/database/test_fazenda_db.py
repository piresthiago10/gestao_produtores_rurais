import pytest
from sqlalchemy import select
from app.models.models import Fazenda, Safra
from app.tests.fixtures.fazenda import farms_in_db
from app.tests.fixtures.safra import crops_in_db

@pytest.mark.asyncio
async def test_create_farm(get_db, crops_in_db):
    """Testa a criação de uma nova fazenda."""
    new_farm = Fazenda(
        nome="Fazenda Horizonte",
        cidade="Uberlândia",
        estado="MG",
        area_total=1000,
        area_agricultavel=700,
        area_vegetacao=300,
        ativo=True,
    )

    get_db.add(new_farm)
    await get_db.commit()
    await get_db.refresh(new_farm)

    crops = await get_db.execute(select(Safra))
    crops = crops.scalars().all()
    
    crops[0].fazenda = new_farm
    crops[1].fazenda = new_farm
    
    # fazenda foi salva corretamenente
    assert new_farm.id is not None
    assert new_farm.nome == "Fazenda Horizonte"
    assert new_farm.cidade == "Uberlândia"
    assert new_farm.area_total == 1000
    assert new_farm.ativo is True
    assert new_farm.safra[0].nome == "Safra de Soja 2023"
    assert new_farm.safra[1].nome == "Safra de Milho 2022"

@pytest.mark.asyncio
async def test_get_farms(get_db, farms_in_db):
    """Testa a obtenção de todas as fazendas."""
    result = await get_db.execute(select(Fazenda))
    farms = result.scalars().all()
    assert len(farms) == 3

@pytest.mark.asyncio
async def test_get_farm_by_id(get_db, farms_in_db):
    """Testa a obtenção de uma fazenda pelo ID."""
    result = await get_db.execute(select(Fazenda).where(Fazenda.id == 1))
    farm = result.scalars().first()
    assert farm is not None

@pytest.mark.asyncio    
async def test_get_farm_by_name(get_db, farms_in_db):
    """Testa a obtenção de uma fazenda pelo nome."""
    result = await get_db.execute(select(Fazenda).filter(Fazenda.nome == "Fazenda Primavera"))
    farm = result.scalars().first()
    assert farm is not None
    
    # Fazenda nao encontrada
    result = await get_db.execute(select(Fazenda).where(Fazenda.nome == "Fazenda Sul de Minas"))
    farm = result.scalars().first()
    assert farm is None

@pytest.mark.asyncio    
async def test_update_farm(get_db, farms_in_db):
    """Testa a atualização de uma fazenda."""
    result = await get_db.execute(select(Fazenda).where(Fazenda.id == 1))
    farm = result.scalars().first()
    farm.ativo = False
    await get_db.commit()
    result = await get_db.execute(select(Fazenda).where(Fazenda.id == 1))
    farm = result.scalars().first()
    assert farm.ativo is False

@pytest.mark.asyncio    
async def test_delete_farm(get_db, farms_in_db, crops_in_db):
    """Testa a exclusão de uma fazenda."""
    result = await get_db.execute(select(Fazenda).where(Fazenda.id == 1))
    farm = result.scalars().first()
    await get_db.delete(farm)
    await get_db.commit()
    result = await get_db.execute(select(Fazenda).where(Fazenda.id == 1))
    farm = result.scalars().first()
    assert farm is None

    # fazenda possui safra, a safra deve ser excluida
    result = await get_db.execute(select(Fazenda).where(Fazenda.id == 2))
    farm_with_crop = result.scalars().first()
    result_crops = await get_db.execute(select(Safra))
    crops = result_crops.scalars().all()
    expected_len = len(crops) -2 
    crops[0].fazenda = farm_with_crop
    crops[1].fazenda = farm_with_crop
    await get_db.delete(farm_with_crop)
    await get_db.commit()
    result = await get_db.execute(select(Safra))
    crops = result.scalars().all()
    assert len(crops) == expected_len
