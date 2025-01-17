import pytest
from sqlalchemy.orm import Session
from app.models.fazenda import Fazenda

@pytest.fixture(scope="function")
def farms_in_db(db: Session):
    """Fixture para criar três fazendas no banco de dados para os testes."""
    farms = [
        Fazenda(
            nome="Fazenda Primavera",
            cidade="Ribeirão Preto",
            estado="SP",
            area_total=500,
            area_agricultavel=300,
            area_vegetacao=200,
            ativo=True,
        ),
        Fazenda(
            nome="Fazenda Sol Nascente",
            cidade="São José do Rio Preto",
            estado="SP",
            area_total=750,
            area_agricultavel=500,
            area_vegetacao=250,
            ativo=True,
        ),
        Fazenda(
            nome="Fazenda Horizonte",
            cidade="Uberlândia",
            estado="MG",
            area_total=1000,
            area_agricultavel=700,
            area_vegetacao=300,
            ativo=False,
        )
    ]

    db.add_all(farms)
    db.commit()
    for farm in farms:
        db.refresh(farm)

    return farms
