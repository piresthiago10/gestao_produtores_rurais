import pytest
from unittest import mock
from app.main import app
from app.tests.mocks.produtor.mocks import VALID_PRODUCER_DATA
from async_asgi_testclient import TestClient

from app.tests.mocks.services.produtor_mocks import (
    RESULT_PRODUCER_WITH_FARM,
    RESULT_PRODUCER_WITHOUT_FARM,
)

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_producer():
    """Testa a criação de um novo produtor."""
    data = VALID_PRODUCER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.produtor.Produtor.create") as create_mock:
            create_mock.return_value = data
            response = await client.post("/produtor/", json=data)
            assert response.status_code == 201
            assert response.json() == data

            create_mock.side_effect = Exception("Erro ao criar o produtor")
            response = await client.post("/produtor/", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao criar o produtor"}


@pytest.mark.asyncio
async def test_get_all_producers():
    """Testa a busca de todos os produtores."""
    data = VALID_PRODUCER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.produtor.Produtor.get_all") as get_mock:
            get_mock.return_value = [data]
            response = await client.get("/produtor/")
            assert response.status_code == 200
            assert response.json() == [data]

            get_mock.side_effect = Exception("Erro ao buscar os produtores")
            response = await client.get("/produtor/")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar os produtores"}


@pytest.mark.asyncio
async def test_get_producer_by_id():
    """Testa a busca de um produtor pelo id."""
    data = VALID_PRODUCER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.produtor.Produtor.get_by_id") as get_mock:
            get_mock.return_value = data
            response = await client.get("/produtor/1")
            assert response.status_code == 200
            assert response.json() == data

            get_mock.side_effect = Exception("Erro ao buscar o produtor")
            response = await client.get("/produtor/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar o produtor"}


@pytest.mark.asyncio
async def test_get_producer_cpf_cnpj():
    """Testa a busca de um produtor pelo cpf_cnpj."""
    data = VALID_PRODUCER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.produtor.Produtor.get_by_cpf_cnpj") as get_mock:
            get_mock.return_value = data
            response = await client.get("/produtor/cpf_cnpj/93231382076")
            assert response.status_code == 200
            assert response.json() == data

            get_mock.side_effect = Exception("Erro ao buscar o produtor")
            response = await client.get("/produtor/cpf_cnpj/93231382076")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao buscar o produtor"}


@pytest.mark.asyncio
async def test_update_producer():
    """Testa a atualização de um produtor."""
    data = VALID_PRODUCER_DATA.copy()
    async with TestClient(app) as client:
        with mock.patch("app.services.produtor.Produtor.update") as update_mock:
            update_mock.return_value = data
            response = await client.put("/produtor/1", json=data)
            assert response.status_code == 200
            assert response.json() == data

            update_mock.side_effect = Exception("Erro ao atualizar o produtor")
            response = await client.put("/produtor/1", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao atualizar o produtor"}


@pytest.mark.asyncio
async def test_delete_producer():
    """Testa a exclusão de um produtor."""
    async with TestClient(app) as client:
        with mock.patch("app.services.produtor.Produtor.delete") as delete_mock:
            delete_mock.return_value = None
            response = await client.delete("/produtor/1")
            assert response.status_code == 200

            delete_mock.side_effect = Exception("Erro ao excluir o produtor")
            response = await client.delete("/produtor/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao excluir o produtor"}


@pytest.mark.asyncio
async def test_soft_delete_producer():
    """Testa a inativação de um produtor."""
    async with TestClient(app) as client:
        with mock.patch(
            "app.services.produtor.Produtor.soft_delete"
        ) as soft_delete_mock:
            soft_delete_mock.return_value = None
            response = await client.put("/produtor/ativo/1")
            assert response.status_code == 200

            soft_delete_mock.side_effect = Exception("Erro ao inativar o produtor")
            response = await client.put("/produtor/ativo/1")
            assert response.status_code == 400
            assert response.json() == {"detail": "Erro ao inativar o produtor"}


@pytest.mark.asyncio
async def test_handle_farm_in_producer():
    """Testa a associação de um produtor com uma fazenda."""
    async with TestClient(app) as client:
        with mock.patch(
            "app.services.produtor.Produtor.handle_farm_in_producer"
        ) as handle_mock:
            handle_mock.return_value = RESULT_PRODUCER_WITH_FARM.copy()
            response = await client.put("/produtor/handle_farm_in_producer/add/1/1")
            assert response.status_code == 200
            assert response.json() == RESULT_PRODUCER_WITH_FARM.copy()

            handle_mock.side_effect = Exception(
                "Erro ao associar o produtor com a fazenda"
            )
            response = await client.put("/produtor/handle_farm_in_producer/add/1/1")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Erro ao associar o produtor com a fazenda"
            }


@pytest.mark.asyncio
async def test_handle_farm_in_producer_remove():
    """Testa a desassociação de um produtor com uma fazenda."""
    async with TestClient(app) as client:
        with mock.patch(
            "app.services.produtor.Produtor.handle_farm_in_producer"
        ) as handle_mock:
            handle_mock.return_value = RESULT_PRODUCER_WITHOUT_FARM.copy()
            response = await client.put("/produtor/handle_farm_in_producer/remove/1/1")
            assert response.status_code == 200
            assert response.json() == RESULT_PRODUCER_WITHOUT_FARM.copy()

            handle_mock.side_effect = Exception(
                "Erro ao desassociar o produtor com a fazenda"
            )
            response = await client.put("/produtor/handle_farm_in_producer/remove/1/1")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Erro ao desassociar o produtor com a fazenda"
            }
