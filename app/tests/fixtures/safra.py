import pytest
from sqlalchemy.orm import Session
from app.models.safra import Safra

@pytest.fixture(scope="function")
def crops_in_db(db: Session):
    """Fixture para criar três safras no banco de dados para os testes."""
    crops = [
        Safra(
            nome="Safra de Soja 2023",
            tipo_cultura="Soja",
            variedade="Orgânico",
            ano_plantio=2023,
            ano_colheita=2024,
            produtividade_tonelada=50.5,
            ativo=True
        ),
        Safra(
            nome="Safra de Milho 2022",
            tipo_cultura="Milho",
            variedade="Híbrido",
            ano_plantio=2022,
            ano_colheita=2023,
            produtividade_tonelada=80.2,
            ativo=False
        ),
        Safra(
            nome="Safra de Trigo 2021",
            tipo_cultura="Trigo",
            variedade="Transgênico",
            ano_plantio=2021,
            ano_colheita=2022,
            produtividade_tonelada=40.7,
            ativo=True
        )
    ]

    db.add_all(crops)
    db.commit()
    for crop in crops:
        db.refresh(crop)

    return crops
