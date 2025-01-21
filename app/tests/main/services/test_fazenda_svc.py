import pytest
from unittest import mock

import sqlalchemy
from app.services.fazenda import Fazenda as FazendaService
from app.services.safra import Safra as SafraService
from app.models.models import Fazenda, Safra
from app.database.crud_fazenda import CRUD_Fazenda
from app.database.crud_safra import CRUD_Safra
from app.tests.fixtures.fazenda import farms_in_db
from app.tests.fixtures.safra import crops_in_db
from app.tests.mocks.services.fazenda_mocks import (
    DASHBOARD_DATA,
    RESULT_FARM_WITH_CROPS,
    RESULT_FARM_WITHOUT_CROPS,
)


@pytest.mark.asyncio
async def test_create_fazenda(get_db):
    """Testa a criação de uma safra."""
    crud = CRUD_Fazenda(get_db)
    service = FazendaService(Fazenda, crud)

    data = {
        "nome": "Fazenda de Soja 2023",
        "cidade": "Uberlândia",
        "estado": "MG",
        "area_agricultavel": 100,
        "area_vegetacao": 50,
        "area_total": 150,
        "ativo": True,
    }
    result = await service.create(data)

    # fazenda foi salva corretamenente
    assert result.id is not None
    assert result.nome == "Fazenda de Soja 2023"
    assert result.ativo is True

    # area total menor que area agricultavel e vegetacao
    data_area_total = data.copy()
    data_area_total["area_total"] = 50
    with pytest.raises(ValueError) as excinfo:
        await service.create(data_area_total)
    excinfo.match(
        "A soma das áreas agricultável e de vegetação não pode exceder a área total da fazenda."
    )

    # criação falhou
    with mock.patch("app.database.crud.CRUD.create") as create_mock:
        create_mock.side_effect = Exception("Erro ao criar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.create(data)
        excinfo.match("Erro ao criar o dado")


@pytest.mark.asyncio
async def test_get_all_farms(get_db, farms_in_db):
    """Testa a obtenção de todas as fazendas."""
    crud = CRUD_Fazenda(get_db)
    service = FazendaService(Fazenda, crud)
    result = await service.get_all()
    assert len(result) == 3

    # erro ao buscar
    with mock.patch("app.database.crud.CRUD.get_all") as get_all_mock:
        get_all_mock.side_effect = Exception("Erro ao buscar os dados")
        with pytest.raises(Exception) as excinfo:
            await service.get_all()
        excinfo.match("Erro ao buscar os dados")


@pytest.mark.asyncio
async def test_get_by_id(get_db, farms_in_db):
    """Testa a obtenção de uma fazenda pelo id."""
    crud = CRUD_Fazenda(get_db)
    service = FazendaService(Fazenda, crud)
    result = await service.get_by_id(1)
    assert result.id == 1

    # id nao encontrado
    result_none = await service.get_by_id(1000)
    assert result_none is None

    # erro ao buscar
    with mock.patch("app.database.crud.CRUD.get_by_id") as get_by_id_mock:
        get_by_id_mock.side_effect = Exception("Erro ao buscar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.get_by_id(1)
        excinfo.match("Erro ao buscar o dado")


@pytest.mark.asyncio
async def test_update_farm(get_db, farms_in_db):
    """Testa a atualização de uma fazenda."""
    crud = CRUD_Fazenda(get_db)
    service = FazendaService(Fazenda, crud)
    data = {
        "nome": "Fazenda de Soja 2025",
        "cidade": "Uberlândia",
        "estado": "MG",
        "area_agricultavel": 100,
        "area_vegetacao": 50,
        "area_total": 150,
        "ativo": True,
    }
    result = await service.update(1, data)
    assert result.nome == "Fazenda de Soja 2025"

    # area total menor que area agricultavel e vegetacao
    data_area_total = data.copy()
    data_area_total["area_total"] = 50
    with pytest.raises(ValueError) as excinfo:
        await service.update(1, data_area_total)
    excinfo.match(
        "A soma das áreas agricultável e de vegetação não pode exceder a área total da fazenda."
    )

    # atualizacao falhou
    with mock.patch("app.database.crud.CRUD.update") as update_mock:
        update_mock.side_effect = Exception("Erro ao atualizar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.update(1, data)
        excinfo.match("Erro ao atualizar o dado")

    # atualizar id inexistente
    with pytest.raises(Exception) as excinfo:
        await service.update(1000, data)
    excinfo.match("Dado nao encontrado")


@pytest.mark.asyncio
async def test_get_dashboard(get_db, farms_in_db, crops_in_db):
    """Testa a obtenção do dashboard."""
    farm_crud = CRUD_Fazenda(get_db)
    crop_crud = CRUD_Safra(get_db)
    farm_service = FazendaService(Fazenda, farm_crud)
    crop_service = SafraService(Safra, crop_crud)

    crops = await crop_service.get_all()
    farms = await farm_service.get_all()

    crops[0].fazenda = farms[0]
    crops[1].fazenda = farms[1]
    crops[2].fazenda = farms[2]

    result = await farm_service.get_dashboard_data(Safra)
    assert result == DASHBOARD_DATA


# handle_crop_in_farm
@pytest.mark.asyncio
async def test_handle_crop_in_farm(get_db, farms_in_db, crops_in_db):
    """Testa a obtenção do dashboard."""
    farm_crud = CRUD_Fazenda(get_db)
    farm_service = FazendaService(Fazenda, farm_crud)

    result = await farm_service.handle_crop_in_farm(Safra, 1, 1)
    assert result == RESULT_FARM_WITH_CROPS

    # id fazenda inexistente
    with pytest.raises(Exception) as excinfo:
        await farm_service.handle_crop_in_farm(Safra, 1000, 1)
    excinfo.match("Fazenda com ID 1000 não encontrada.")

    # id safra inexistente
    with pytest.raises(Exception) as excinfo:
        await farm_service.handle_crop_in_farm(Safra, 1, 1000)
    excinfo.match("Safra com ID 1000 não encontrada.")

    # removendo safra da fazenda
    result = await farm_service.handle_crop_in_farm(Safra, 1, 1, is_add=False)
    assert result == RESULT_FARM_WITHOUT_CROPS
