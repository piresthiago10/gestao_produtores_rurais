import pytest
from unittest import mock

import sqlalchemy
from app.services.safra import Safra as SafraService
from app.models.models import Safra
from app.database.crud_safra import CRUD_Safra
from app.tests.fixtures.safra import crops_in_db


@pytest.mark.asyncio
async def test_create_safra(get_db):
    """Testa a criação de uma safra."""
    crud = CRUD_Safra(get_db)
    service = SafraService(Safra, crud)

    data = {
        "nome": "Safra de Soja 2023",
        "tipo_cultura": "Soja",
        "variedade": "Orgânico",
        "ano_plantio": 2023,
        "ano_colheita": 2024,
        "produtividade_tonelada": 50.5,
        "ativo": True,
    }
    result = await service.create(data)

    # safra foi salva corretamenente
    assert result.id is not None
    assert result.nome == "Safra de Soja 2023"
    assert result.ativo is True

    # criação falhou
    with mock.patch("app.database.crud_safra.CRUD.create") as create_mock:
        create_mock.side_effect = Exception("Erro ao criar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.create(data)
        excinfo.match("Erro ao criar o dado")


@pytest.mark.asyncio
async def test_get_by_id(get_db, crops_in_db):
    """Testa a busca de uma safra pelo id."""
    crud = CRUD_Safra(get_db)
    service = SafraService(Safra, crud)
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
async def test_get_by_id(get_db, crops_in_db):
    """Testa a busca de uma safra pelo id."""
    crud = CRUD_Safra(get_db)
    service = SafraService(Safra, crud)
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
async def test_update(get_db, crops_in_db):
    """Testa a atualização de um dado."""
    crud = CRUD_Safra(get_db)
    service = SafraService(Safra, crud)
    data = {
        "nome": "Safra de Soja 2025",
        "tipo_cultura": "Soja",
        "variedade": "Orgânico",
        "ano_plantio": 2023,
        "ano_colheita": 2024,
        "produtividade_tonelada": 50.5,
        "ativo": True,
    }
    result = await service.update(1, data)
    assert result.nome == "Safra de Soja 2025"

    # atualização falhou
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
async def test_delete(get_db, crops_in_db):
    """Testa a exclusão de um dado."""
    crud = CRUD_Safra(get_db)
    service = SafraService(Safra, crud)
    result = await service.delete(1)
    assert result is True

    # exclusão falhou
    with mock.patch("app.database.crud.CRUD.delete") as delete_mock:
        delete_mock.side_effect = Exception("Erro ao excluir o dado")
        with pytest.raises(Exception) as excinfo:
            await service.delete(1)
        excinfo.match("Erro ao excluir o dado")

    # excluir id inexistente
    with pytest.raises(Exception) as excinfo:
        await service.delete(1000)
    excinfo.match("Dado nao encontrado")


@pytest.mark.asyncio
async def test_soft_delete(get_db, crops_in_db):
    """Testa a inativação de um dado."""
    crud = CRUD_Safra(get_db)
    service = SafraService(Safra, crud)
    result = await service.soft_delete(1)
    assert result is True

    # inativação falhou
    with mock.patch("app.database.crud.CRUD.soft_delete") as soft_delete_mock:
        soft_delete_mock.side_effect = Exception("Erro ao inativar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.soft_delete(1)
        excinfo.match("Erro ao inativar o dado")

    # inativar id inexistente
    with pytest.raises(Exception) as excinfo:
        await service.soft_delete(1000)
    excinfo.match("Dado nao encontrado")
