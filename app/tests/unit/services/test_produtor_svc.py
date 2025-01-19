import pytest
from unittest import mock

import sqlalchemy
from app.services.produtor import Produtor as ProdutorService
from app.models.models import Produtor
from app.database.crud_produtor import CRUD_Produtor
from app.tests.fixtures.produtor import producers_in_db

@pytest.mark.asyncio
async def test_create_produtor(get_db):
    """Testa a criação de um produtor."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    data = {
        "nome": "Bruno Lima",
        "cpf_cnpj": "93231382076",
        "telefone": "11985768364",
        "email": "bruno.lima@teste.com.br",
        "senha": "123Abc!!",
        "tipo": "comum",
        "ativo": True
    }
    result = await produtor_service.create(data)
    assert result.id
    
    
    # produtor ja cadastrado
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await produtor_service.create(data)
    
    # produtor não pode ser do tipo admin
    data_admin = data.copy()
    data_admin["tipo"] = "admin"
    with pytest.raises(ValueError) as excinfo:
        await produtor_service.create(data_admin)
    excinfo.match("Produtor não pode ser do tipo admin")
    
    # criação falhou
    with mock.patch("app.database.crud.CRUD.create") as create_mock:
        create_mock.side_effect = Exception("Erro ao criar o dado")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.create(data)
        excinfo.match("Erro ao criar o dado")
        
@pytest.mark.asyncio
async def test_get_by_id(get_db, producers_in_db):
    """Testa a busca de um produtor pelo id."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    result = await produtor_service.get_by_id(1)
    assert result.id == 1
    
    # id não encontrado
    result_none = await produtor_service.get_by_id(1000)
    assert result_none is None
    
    # erro ao buscar
    with mock.patch("app.database.crud.CRUD.get_by_id") as get_by_id_mock:
        get_by_id_mock.side_effect = Exception("Erro ao buscar o dado")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.get_by_id(1)
        excinfo.match("Erro ao buscar o dado")
    
@pytest.mark.asyncio
async def test_get_by_email(get_db, producers_in_db):
    """Testa a busca de um produtor pelo email."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    result = await produtor_service.get_by_email("bruno.lima@teste.com.br")
    assert result.email == "bruno.lima@teste.com.br"
    
    # email não encontrado
    result_none = await produtor_service.get_by_email("nao_existe@teste.com.br")
    assert result_none is None
    
    # erro ao buscar
    with mock.patch("app.database.crud_produtor.CRUD_Produtor.get_by_email") as get_by_email_mock:
        get_by_email_mock.side_effect = Exception("Erro ao buscar o dado")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.get_by_email("bruno.lima@teste.com.br")
        excinfo.match("Erro ao buscar o dado")

@pytest.mark.asyncio
async def test_get_by_cpf_cnpj(get_db, producers_in_db):
    """Testa a busca de um produtor pelo cpf_cnpj."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    result = await produtor_service.get_by_cpf_cnpj("11223344556")
    assert result.cpf_cnpj == "11223344556"
    
    # cpf_cnpj não encontrado
    result_none = await produtor_service.get_by_cpf_cnpj("93231382076")
    assert result_none is None
    
    # erro ao buscar
    with mock.patch(
        "app.database.crud_produtor.CRUD_Produtor.get_by_cpf_cnpj") as get_by_cpf_cnpj_mock:
        get_by_cpf_cnpj_mock.side_effect = Exception("Erro ao buscar o dado")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.get_by_cpf_cnpj("93231382076")
        excinfo.match("Erro ao buscar o dado")

@pytest.mark.asyncio
async def test_get_all_produtors(get_db, producers_in_db):
    """Testa a busca de todos os produtors."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    result = await produtor_service.get_all()
    assert len(result) > 0
    
    # erro ao buscar
    with mock.patch("app.database.crud.CRUD.get_all") as get_all_mock:
        get_all_mock.side_effect = Exception("Erro ao buscar os dados")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.get_all()
        excinfo.match("Erro ao buscar os dados")
    
@pytest.mark.asyncio
async def test_update(get_db, producers_in_db):
    """Testa a atualização de um produtor."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    data = {
        "nome": "Bruno Lima",
        "cpf_cnpj": "93231382076",
        "telefone": "11985768364",
        "email": "bruno.lima@teste.com.br",
        "senha": "123Abc!!",
        "tipo": "comum",
        "ativo": True
    }
    result = await produtor_service.update(1, data)
    assert result.id == 1
    
    # produtor não pode ser do tipo admin
    data_admin = data.copy()
    data_admin["tipo"] = "admin"
    with pytest.raises(ValueError) as excinfo:
        await produtor_service.update(1, data_admin)
    excinfo.match("Produtor não pode ser do tipo admin")
    
    # atualizar id inexistente
    with pytest.raises(Exception) as excinfo:
        await produtor_service.update(1000, data)
    excinfo.match("Dado nao encontrado")
    
    # atualização falhou
    with mock.patch("app.database.crud.CRUD.update") as update_mock:
        update_mock.side_effect = Exception("Erro ao atualizar o dado")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.update(1, data)
        excinfo.match("Erro ao atualizar o dado")

@pytest.mark.asyncio
async def test_delete(get_db, producers_in_db):
    """Testa a exclusão de um produtor."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    result = await produtor_service.delete(1)
    assert result is True
    
    # excluir id inexistente
    with pytest.raises(Exception) as excinfo:
        await produtor_service.delete(1000)
    excinfo.match("Dado nao encontrado")
    
    # exclusão falhou
    with mock.patch("app.database.crud.CRUD.delete") as delete_mock:
        delete_mock.side_effect = Exception("Erro ao excluir o dado")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.delete(1)
        excinfo.match("Erro ao excluir o dado")
        
@pytest.mark.asyncio
async def test_soft_delete(get_db, producers_in_db):
    """Testa a inativação de um produtor."""
    crud = CRUD_Produtor(get_db)
    produtor_service = ProdutorService(Produtor, crud)
    result = await produtor_service.soft_delete(1)
    assert result is True
    
    # inativação falhou
    with mock.patch("app.database.crud.CRUD.soft_delete") as soft_delete_mock:
        soft_delete_mock.side_effect = Exception("Erro ao inativar o dado")
        with pytest.raises(Exception) as excinfo:
            await produtor_service.soft_delete(1)
        excinfo.match("Erro ao inativar o dado")