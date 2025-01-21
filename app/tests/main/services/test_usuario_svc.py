import pytest
from unittest import mock

import sqlalchemy
from app.services.usuario import Usuario as UsuarioService
from app.models.models import Usuario
from app.database.crud_usuario import CRUD_Usuario
from app.tests.fixtures.usuario import users_in_db


@pytest.mark.asyncio
async def test_create_user(get_db):
    """Testa a criação de um novo usuário."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
    data = {
        "nome": "Pedro da Silva",
        "cpf_cnpj": "93231382076",
        "telefone": "11985768364",
        "email": "pedro.silva@teste.com.br",
        "senha": "123Abc!!",
        "tipo": "comum",
        "ativo": True,
    }
    result = await service.create(data)
    assert result.id

    # usuario ja cadastrado
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await service.create(data)

    # criação falhou
    with mock.patch("app.database.crud.CRUD.create") as create_mock:
        create_mock.side_effect = Exception("Erro ao criar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.create(data)
        excinfo.match("Erro ao criar o dado")


@pytest.mark.asyncio
async def test_get_by_id(get_db, users_in_db):
    """Testa a busca de um usuário pelo id."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
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
async def test_get_by_cpf_cnpj(get_db, users_in_db):
    """Testa a busca de um usuário pelo cpf_cnpj."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
    result = await service.get_by_cpf_cnpj("98765432100")
    assert result.cpf_cnpj == "98765432100"

    # cpf_cnpj não encontrado
    result_none = await service.get_by_cpf_cnpj("93231382076")
    assert result_none is None

    # erro ao buscar
    with mock.patch(
        "app.database.crud_usuario.CRUD_Usuario.get_by_cpf_cnpj"
    ) as get_by_cpf_cnpj_mock:
        get_by_cpf_cnpj_mock.side_effect = Exception("Erro ao buscar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.get_by_cpf_cnpj("93231382076")
        excinfo.match("Erro ao buscar o dado")


@pytest.mark.asyncio
async def test_get_by_email(get_db, users_in_db):
    """Testa a busca de um usuário pelo email."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
    result = await service.get_by_email("maria.oliveira@teste.com.br")
    assert result.email == "maria.oliveira@teste.com.br"

    # email nao encontrado
    result_none = await service.get_by_email("pedro.silva@teste.com.br")
    assert result_none is None

    # erro ao buscar
    with mock.patch(
        "app.database.crud_usuario.CRUD_Usuario.get_by_email"
    ) as get_by_email_mock:
        get_by_email_mock.side_effect = Exception("Erro ao buscar o dado")
        with pytest.raises(Exception) as excinfo:
            await service.get_by_email("pedro.silva@teste.com.br")
        excinfo.match("Erro ao buscar o dado")


@pytest.mark.asyncio
async def test_get_all_usuarios(get_db, users_in_db):
    """Testa a busca de todos os usuarios."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
    result = await service.get_all()
    assert len(result) == 3

    # erro ao buscar
    with mock.patch("app.database.crud.CRUD.get_all") as get_all_mock:
        get_all_mock.side_effect = Exception("Erro ao buscar os dados")
        with pytest.raises(Exception) as excinfo:
            await service.get_all()
        excinfo.match("Erro ao buscar os dados")


@pytest.mark.asyncio
async def test_update(get_db, users_in_db):
    """Testa a atualização de um dado."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
    data = {
        "nome": "Pedro da Silva",
        "cpf_cnpj": "93231382076",
        "telefone": "11985768364",
        "email": "pedro.silva@teste.com.br",
        "senha": "123Abc!!",
        "tipo": "comum",
        "ativo": True,
    }
    result = await service.update(1, data)
    assert result.id == 1

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
async def test_delete(get_db, users_in_db):
    """Testa a exclusão de um dado."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
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
async def test_soft_delete(get_db, users_in_db):
    """Testa a inativação de um dado."""
    crud = CRUD_Usuario(get_db)
    service = UsuarioService(Usuario, crud)
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
