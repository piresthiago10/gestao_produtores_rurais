import pytest
from unittest import mock
from app.main import app
from app.tests.mocks.safra.mocks import VALID_CROP_DATA
from async_asgi_testclient import TestClient

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_crop():
    """Testa a criação de uma nova safra."""
    data = VALID_CROP_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.safra.Safra.create") as create_mock:
            create_mock.return_value = data
            response = await client.post("/safra/", json=data)
            assert response.status_code == 201
            assert response.json() == data

            create_mock.side_effect = Exception("Erro ao criar a safra")
            response = await client.post("/safra/", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao criar a safra"}


@pytest.mark.asyncio
async def test_get_all_crops():
    """Testa a busca de todas as safra."""
    data = VALID_CROP_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.safra.Safra.get_all") as get_mock:
            get_mock.return_value = [data]
            response = await client.get("/safra/")
            assert response.status_code == 200
            assert response.json() == [data]

            get_mock.side_effect = Exception("Erro ao buscar as safra")
            response = await client.get("/safra/")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar as safra"}


@pytest.mark.asyncio
async def test_get_crop_by_id():
    """Testa a busca de uma safra pelo id."""
    data = VALID_CROP_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.safra.Safra.get_by_id") as get_mock:
            get_mock.return_value = data
            response = await client.get("/safra/1")
            assert response.status_code == 200
            assert response.json() == data

            get_mock.side_effect = Exception("Erro ao buscar a safra")
            response = await client.get("/safra/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar a safra"}


@pytest.mark.asyncio
async def test_delete_crop():
    """Testa a exclusão de uma safra."""
    async with TestClient(app) as client:
        with mock.patch("app.services.safra.Safra.delete") as delete_mock:
            delete_mock.return_value = True
            response = await client.delete("/safra/1")
            assert response.status_code == 200
            assert response.json() is True

            delete_mock.side_effect = Exception("Erro ao excluir a safra")
            response = await client.delete("/safra/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao excluir a safra"}


@pytest.mark.asyncio
async def test_soft_delete_crop():
    """Testa a exclusão de uma safra."""
    async with TestClient(app) as client:
        with mock.patch("app.services.safra.Safra.soft_delete") as delete_mock:
            delete_mock.return_value = True
            response = await client.put("/safra/ativo/1")
            assert response.status_code == 200
            assert response.json() is True

            delete_mock.side_effect = Exception("Erro ao excluir a safra")
            response = await client.put("/safra/ativo/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao excluir a safra"}
