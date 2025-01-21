import pytest
from unittest import mock
from app.database.crud import CRUD
from app.models.models import Usuario
from app.tests.fixtures.usuario import users_in_db


@pytest.mark.asyncio
async def test_create(get_db):
    """Testa a criação de um novo dado no banco de dados."""
    crud = CRUD(get_db)
    data = {
        "nome": "Pedro da Silva",
        "cpf_cnpj": "93231382076",
        "telefone": "11985768364",
        "email": "pedro.silva@teste.com.br",
        "senha": "123Abc!!",
        "tipo": "comum",
        "ativo": True,
    }
    result = await crud.create(Usuario, data)
    assert result.id

    # criação falhou
    with mock.patch("app.database.crud.CRUD.create") as create_mock:
        create_mock.side_effect = Exception("Erro ao criar o dado")
        with pytest.raises(Exception) as excinfo:
            await crud.create(Usuario, data)
        excinfo.match("Erro ao criar o dado")


@pytest.mark.asyncio
async def test_get_by_id(get_db, users_in_db):
    """Testa a busca de um dado pelo id."""
    crud = CRUD(get_db)
    result = await crud.get_by_id(Usuario, 1)
    assert result.id == 1

    # dado nao encontrado
    with mock.patch("app.database.crud.CRUD.get_by_id") as get_by_id_mock:
        get_by_id_mock.side_effect = Exception("Erro genérico")
        with pytest.raises(Exception) as excinfo:
            await crud.get_by_id(Usuario, 1)
        excinfo.match("Erro genérico")


@pytest.mark.asyncio
async def test_get_all(get_db, users_in_db):
    """Testa a busca de todos os dados."""
    crud = CRUD(get_db)
    result = await crud.get_all(Usuario)
    assert len(result) == 3

    # dados nao encontrados
    with mock.patch("app.database.crud.CRUD.get_all") as get_all_mock:
        get_all_mock.side_effect = Exception("Erro genérico")
        with pytest.raises(Exception) as excinfo:
            await crud.get_all(Usuario)
        excinfo.match("Erro genérico")


@pytest.mark.asyncio
async def test_update(get_db, users_in_db):
    """Testa a atualização de um dado."""
    crud = CRUD(get_db)
    data = await crud.get_by_id(Usuario, 3)
    assert data.ativo == True
    data.ativo = False
    result = await crud.update(Usuario, 3, data)
    assert result.id == 3
    assert result.ativo == False

    # atualização falhou
    with mock.patch("app.database.crud.CRUD.update") as update_mock:
        update_mock.side_effect = Exception("Erro ao atualizar o dado")
        with pytest.raises(Exception) as excinfo:
            await crud.update(Usuario, 1, data)
        excinfo.match("Erro ao atualizar o dado")


@pytest.mark.asyncio
async def test_delete(get_db, users_in_db):
    """Testa a exclusão de um dado."""
    crud = CRUD(get_db)
    result = await crud.delete(Usuario, 1)
    assert result is True

    # exclusão falhou
    with mock.patch("app.database.crud.CRUD.delete") as delete_mock:
        delete_mock.side_effect = Exception("Erro ao excluir o dado")
        with pytest.raises(Exception) as excinfo:
            await crud.delete(Usuario, 1)
        excinfo.match("Erro ao excluir o dado")


@pytest.mark.asyncio
async def test_soft_delete(get_db, users_in_db):
    """Testa a inativação de um dado."""
    crud = CRUD(get_db)
    result = await crud.soft_delete(Usuario, 1)
    assert result is True

    # inativação falhou
    with mock.patch("app.database.crud.CRUD.soft_delete") as soft_delete_mock:
        soft_delete_mock.side_effect = Exception("Erro ao inativar o dado")
        with pytest.raises(Exception) as excinfo:
            await crud.soft_delete(Usuario, 1)
        excinfo.match("Erro ao inativar o dado")
