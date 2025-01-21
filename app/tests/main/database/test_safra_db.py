import pytest
from sqlalchemy import select
from app.models.models import Safra
from app.tests.fixtures.safra import crops_in_db


@pytest.mark.asyncio
async def test_create_safra(get_db):
    """Testa a criação de uma safra."""
    new_crop = Safra(
        nome="Safra de Soja 2023",
        tipo_cultura="Soja",
        variedade="Orgânico",
        ano_plantio=2023,
        ano_colheita=2024,
        produtividade_tonelada=50.5,
        ativo=True,
    )
    get_db.add(new_crop)
    await get_db.commit()
    await get_db.refresh(new_crop)

    # safra foi salva corretamenente
    assert new_crop.id is not None
    assert new_crop.nome == "Safra de Soja 2023"
    assert new_crop.ativo is True


@pytest.mark.asyncio
async def test_get_safras(get_db, crops_in_db):
    """Testa a obtenção de uma safra."""
    result = await get_db.execute(select(Safra))
    farms = result.scalars().all()
    assert len(farms) == 3


@pytest.mark.asyncio
async def test_get_safra_by_name(get_db, crops_in_db):
    """Testa a obtenção de uma safra pelo nome."""
    result = await get_db.execute(
        select(Safra).where(Safra.nome == "Safra de Soja 2023")
    )
    crop = result.scalars().first()
    assert crop is not None


@pytest.mark.asyncio
async def test_update_safra(get_db, crops_in_db):
    """Testa a atualização de uma safra."""
    result = await get_db.execute(select(Safra).where(Safra.id == 1))
    crop = result.scalars().first()
    crop.ativo = False
    await get_db.commit()
    result = await get_db.execute(select(Safra).where(Safra.id == 1))
    crop = result.scalars().first()
    assert crop.ativo is False


@pytest.mark.asyncio
async def test_delete_safra(get_db, crops_in_db):
    """Testa a exclusão de uma safra."""
    result = await get_db.execute(select(Safra).where(Safra.id == 1))
    crop = result.scalars().first()
    await get_db.delete(crop)
    await get_db.commit()
    result = await get_db.execute(select(Safra).where(Safra.id == 1))
    crop = result.scalars().first()
    assert crop is None
