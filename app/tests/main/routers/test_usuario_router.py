import pytest
from unittest import mock
from app.main import app
from app.tests.mocks.usuario.mocks import (
    VALID_USER_DATA,
    VALID_USER_DATA_WITH_SENHA_HASH,
    VALID_USER_DATA_WITHOUT_SENHA_HASH,
)
from async_asgi_testclient import TestClient

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_user():
    """Testa a criação de um novo usuário."""
    data = VALID_USER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.usuario.Usuario.create") as create_mock:
            create_mock.return_value = VALID_USER_DATA_WITH_SENHA_HASH.copy()
            response = await client.post("/usuario/", json=data)
            assert response.status_code == 201
            assert response.json() == VALID_USER_DATA_WITHOUT_SENHA_HASH.copy()

            create_mock.side_effect = Exception("Erro ao criar o usuario")
            response = await client.post("/usuario/", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao criar o usuario"}


@pytest.mark.asyncio
async def test_get_all_users():
    """Testa a busca de todos os usuarios."""
    data = VALID_USER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.usuario.Usuario.get_all") as get_mock:
            get_mock.return_value = [data]
            response = await client.get("/usuario/")
            assert response.status_code == 200
            assert response.json() == [data]

            get_mock.side_effect = Exception("Erro ao buscar os usuarios")
            response = await client.get("/usuario/")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar os usuarios"}


@pytest.mark.asyncio
async def test_get_user_by_id():
    """Testa a busca de um usuario pelo id."""
    data = VALID_USER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.usuario.Usuario.get_by_id") as get_mock:
            get_mock.return_value = data
            response = await client.get("/usuario/1")
            assert response.status_code == 200
            assert response.json() == data

            get_mock.side_effect = Exception("Erro ao buscar o usuario")
            response = await client.get("/usuario/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar o usuario"}


@pytest.mark.asyncio
async def test_get_user_by_cpf_cnpj():
    """Testa a busca de um usuario pelo cpf_cnpj."""
    data = VALID_USER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.usuario.Usuario.get_by_cpf_cnpj") as get_mock:
            get_mock.return_value = data
            response = await client.get("/usuario/cpf_cnpj/93231382076")
            assert response.status_code == 200
            assert response.json() == data

            get_mock.side_effect = Exception("Erro ao buscar o usuario")
            response = await client.get("/usuario/cpf_cnpj/93231382076")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar o usuario"}


@pytest.mark.asyncio
async def test_update_user():
    """Testa a atualização de um usuario."""
    data = VALID_USER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.usuario.Usuario.update") as update_mock:
            update_mock.return_value = VALID_USER_DATA_WITH_SENHA_HASH.copy()
            response = await client.put("/usuario/1", json=data)
            assert response.status_code == 200
            assert response.json() == VALID_USER_DATA_WITHOUT_SENHA_HASH.copy()

            update_mock.side_effect = Exception("Erro ao atualizar o usuario")
            response = await client.put("/usuario/1", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao atualizar o usuario"}


@pytest.mark.asyncio
async def test_delete_user():
    """Testa a exclusão de um usuario."""
    async with TestClient(app) as client:
        with mock.patch("app.services.usuario.Usuario.delete") as delete_mock:
            delete_mock.return_value = True
            response = await client.delete("/usuario/1")
            assert response.status_code == 200
            assert response.json() is True

            delete_mock.side_effect = Exception("Erro ao excluir o usuario")
            response = await client.delete("/usuario/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao excluir o usuario"}


@pytest.mark.asyncio
async def test_soft_delete_user():
    """Testa a exclusão de um usuario."""
    data = VALID_USER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.usuario.Usuario.soft_delete") as delete_mock:
            delete_mock.return_value = data
            response = await client.put("/usuario/ativo/1")
            assert response.status_code == 200
            assert response.json() == data

            delete_mock.side_effect = Exception("Erro ao excluir o usuario")
            response = await client.put("/usuario/ativo/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao excluir o usuario"}
