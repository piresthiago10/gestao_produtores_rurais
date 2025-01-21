import pytest
from unittest import mock
from app.main import app
from app.tests.mocks.fazenda.mocks import VALID_FARM_DATA
from app.tests.mocks.services.fazenda_mocks import (
    DASHBOARD_DATA,
    RESULT_FARM_WITH_CROPS,
    RESULT_FARM_WITHOUT_CROPS,
)
from async_asgi_testclient import TestClient

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_farm():
    """Testa a criação de uma nova fazenda."""
    data = VALID_FARM_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.fazenda.Fazenda.create") as create_mock:
            create_mock.return_value = data
            response = await client.post("/fazenda/", json=data)
            assert response.status_code == 201
            assert response.json() == data

            create_mock.side_effect = Exception("Erro ao criar a fazenda")
            response = await client.post("/fazenda/", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao criar a fazenda"}


@pytest.mark.asyncio
async def test_get_farm():
    """Testa a busca de todas as fazendas."""
    data = VALID_FARM_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.fazenda.Fazenda.get_all") as get_mock:
            get_mock.return_value = [data]
            response = await client.get("/fazenda/")
            assert response.status_code == 200
            assert response.json() == [data]

            get_mock.side_effect = Exception("Erro ao buscar as fazendas")
            response = await client.get("/fazenda/")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar as fazendas"}


@pytest.mark.asyncio
async def test_get_farm_by_id():
    """Testa a busca de uma fazenda pelo id."""
    data = VALID_FARM_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.fazenda.Fazenda.get_by_id") as get_mock:
            get_mock.return_value = data
            response = await client.get("/fazenda/1")
            assert response.status_code == 200
            assert response.json() == data

            get_mock.side_effect = Exception("Erro ao buscar a fazenda")
            response = await client.get("/fazenda/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar a fazenda"}


@pytest.mark.asyncio
async def test_update_farm():
    """Testa a atualização de uma fazenda."""
    data = VALID_FARM_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.fazenda.Fazenda.update") as update_mock:
            update_mock.return_value = data
            response = await client.put("/fazenda/1", json=data)
            assert response.status_code == 200
            assert response.json() == data

            update_mock.side_effect = Exception("Erro ao atualizar a fazenda")
            response = await client.put("/fazenda/1", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao atualizar a fazenda"}


@pytest.mark.asyncio
async def test_delete_farm():
    """Testa a exclusão de uma fazenda."""
    async with TestClient(app) as client:
        with mock.patch("app.services.fazenda.Fazenda.delete") as delete_mock:
            delete_mock.return_value = True
            response = await client.delete("/fazenda/1")
            assert response.status_code == 200
            assert response.json() is True

            delete_mock.side_effect = Exception("Erro ao excluir a fazenda")
            response = await client.delete("/fazenda/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao excluir a fazenda"}


@pytest.mark.asyncio
async def test_soft_delete_farm():
    """Testa a exclusão de uma fazenda."""
    async with TestClient(app) as client:
        with mock.patch("app.services.fazenda.Fazenda.soft_delete") as delete_mock:
            delete_mock.return_value = True
            response = await client.put("/fazenda/ativo/1")
            assert response.status_code == 200
            assert response.json() is True

            delete_mock.side_effect = Exception("Erro ao excluir a fazenda")
            response = await client.put("/fazenda/ativo/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao excluir a fazenda"}


@pytest.mark.asyncio
async def test_get_farm_dashboard():
    """Testa a busca de todas as fazendas."""
    data = DASHBOARD_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.fazenda.Fazenda.get_dashboard_data") as get_mock:
            get_mock.return_value = data
            response = await client.get("/fazenda/dashboard/data")
            assert response.status_code == 200
            assert response.json() == data

            get_mock.side_effect = Exception("Erro ao buscar as fazendas")
            response = await client.get("/fazenda/dashboard/data")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar as fazendas"}


@pytest.mark.asyncio
async def test_handle_crop_in_farm():
    """Testa a associação de uma safra a uma fazenda."""
    async with TestClient(app) as client:
        with mock.patch(
            "app.services.fazenda.Fazenda.handle_crop_in_farm"
        ) as handle_mock:
            handle_mock.return_value = RESULT_FARM_WITH_CROPS.copy()
            response = await client.put("/fazenda/handle_crop_in_farm/add/1/1")
            assert response.status_code == 200
            assert response.json() == RESULT_FARM_WITH_CROPS.copy()

            handle_mock.side_effect = Exception(
                "Erro ao associar a safra a uma fazenda"
            )
            response = await client.put("/fazenda/handle_crop_in_farm/add/1/1")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Erro ao associar a safra a uma fazenda"
            }


@pytest.mark.asyncio
async def test_handle_crop_in_farm_remove():
    """Testa a associação de uma safra a uma fazenda."""
    async with TestClient(app) as client:
        with mock.patch(
            "app.services.fazenda.Fazenda.handle_crop_in_farm"
        ) as handle_mock:
            handle_mock.return_value = RESULT_FARM_WITHOUT_CROPS.copy()
            response = await client.put("/fazenda/handle_crop_in_farm/remove/1/1")
            assert response.status_code == 200
            assert response.json() == RESULT_FARM_WITHOUT_CROPS.copy()

            handle_mock.side_effect = Exception(
                "Erro ao associar a safra a uma fazenda"
            )
            response = await client.put("/fazenda/handle_crop_in_farm/remove/1/1")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Erro ao associar a safra a uma fazenda"
            }
