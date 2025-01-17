import pytest
from app.models.fazenda import Fazenda
from app.models.safra import Safra
from app.models.produtor import Produtor
from app.tests.fixtures.fazenda import farms_in_db
from app.tests.fixtures.safra import crops_in_db

def test_create_farm(db, crops_in_db):
    """Testa a criação de uma nova fazenda."""
    new_farm = Fazenda(
        nome="Fazenda Horizonte",
        cidade="Uberlândia",
        estado="MG",
        area_total=1000,
        area_agricultavel=700,
        area_vegetacao=300,
        ativo=True,
    )
    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    crops = db.query(Safra).all()
    
    crops[0].fazenda = new_farm
    crops[1].fazenda = new_farm
    
    # fazenda foi salva corretamenente
    assert new_farm.id is not None
    assert new_farm.nome == "Fazenda Horizonte"
    assert new_farm.cidade == "Uberlândia"
    assert new_farm.area_total == 1000
    assert new_farm.ativo is True
    assert new_farm.safra[0].nome == "Safra de Soja 2023"
    assert new_farm.safra[1].nome == "Safra de Milho 2022"

def test_get_farms(db, farms_in_db):
    """Testa a obtenção de todas as fazendas."""
    farms = db.query(Fazenda).all()
    assert len(farms) == 3

def test_get_farm_by_id(db, farms_in_db):
    """Testa a obtenção de uma fazenda pelo ID."""
    farm = db.query(Fazenda).filter(Fazenda.id == 1).first()
    assert farm is not None
    
def test_get_farm_by_name(db, farms_in_db):
    """Testa a obtenção de uma fazenda pelo nome."""
    farm = db.query(Fazenda).filter(Fazenda.nome == "Fazenda Primavera").first()
    assert farm is not None
    
    # Fazenda nao encontrada
    farm = db.query(Fazenda).filter(Fazenda.nome == "Fazenda Sul de Minas").first()
    assert farm is None
    
def test_update_farm(db, farms_in_db):
    """Testa a atualização de uma fazenda."""
    farm = db.query(Fazenda).filter(Fazenda.id == 1).first()
    farm.ativo = False
    db.commit()
    farm = db.query(Fazenda).filter(Fazenda.id == 1).first()
    assert farm.ativo is False
    
def test_delete_farm(db, farms_in_db, crops_in_db):
    """Testa a exclusão de uma fazenda."""
    farm = db.query(Fazenda).filter(Fazenda.id == 1).first()
    db.delete(farm)
    db.commit()
    farm = db.query(Fazenda).filter(Fazenda.id == 1).first()
    assert farm is None

    # fazenda possui safra, a safra deve ser excluida
    farm_with_crop = db.query(Fazenda).filter(Fazenda.id == 2).first()
    crops = db.query(Safra).all()
    expected_len = len(crops) -2 
    crops[0].fazenda = farm_with_crop
    crops[1].fazenda = farm_with_crop
    db.delete(farm_with_crop)
    db.commit()
    crops = db.query(Safra).all()
    assert len(crops) == expected_len
