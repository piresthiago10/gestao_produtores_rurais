import pytest
from app.models.safra import Safra
from app.tests.fixtures.safra import crops_in_db

def test_create_safra(db):
    """Testa a criação de uma safra."""
    new_crop = Safra(
        nome="Safra de Soja 2023",
        tipo_cultura="Soja",
        variedade="Orgânico",
        ano_plantio=2023,
        ano_colheita=2024,
        produtividade_tonelada=50.5,
        ativo=True
    )
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    
    # safra foi salva corretamenente
    assert new_crop.id is not None
    assert new_crop.nome == "Safra de Soja 2023"
    assert new_crop.ativo is True

def test_get_safras(db, crops_in_db):
    """Testa a obtenção de uma safra."""
    farms = db.query(Safra).all()
    assert len(farms) == 3
    
def test_get_safra_by_name(db, crops_in_db):
    """Testa a obtenção de uma safra pelo nome."""
    crop = db.query(Safra).filter(Safra.nome == "Safra de Soja 2023").first()
    assert crop is not None

def test_update_safra(db, crops_in_db):
    """Testa a atualização de uma safra."""
    crop = db.query(Safra).filter(Safra.id == 1).first()
    crop.ativo = False
    db.commit()
    crop = db.query(Safra).filter(Safra.id == 1).first()
    assert crop.ativo is False
    
def test_delete_safra(db, crops_in_db):
    """Testa a exclusão de uma safra."""
    crop = db.query(Safra).filter(Safra.id == 1).first()
    db.delete(crop)
    db.commit()
    crop = db.query(Safra).filter(Safra.id == 1).first()
    assert crop is None