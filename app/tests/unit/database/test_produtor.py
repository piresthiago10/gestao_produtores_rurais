import pytest
from sqlalchemy.exc import IntegrityError
from app.models.produtor import Produtor
from app.models.fazenda import Fazenda
from app.tests.fixtures.produtor import producers_in_db
from app.tests.fixtures.fazenda import farms_in_db

def test_create_producer(db, farms_in_db):
    """Testa a criação de um novo produtor."""
    new_producer = Produtor(
        nome = "Pedro da Silva",
        cpf_cnpj = "93231382076",
        telefone = "11985768364",
        email = "pedro.silva@teste.com.br",
        senha = "123Abc!!",
        tipo = "comum",
        ativo = True
    )
    
    farms = db.query(Fazenda).all()
    
    farms[0].produtor = new_producer
    farms[1].produtor = new_producer

    db.add(new_producer)
    db.commit()
    db.refresh(new_producer)

    # usuário foi salvo corretamenente
    assert new_producer.id is not None
    assert new_producer.nome == "Pedro da Silva"
    assert new_producer.email == "pedro.silva@teste.com.br"
    assert new_producer.tipo == "comum"
    assert new_producer.ativo is True
    assert new_producer.fazenda[0].nome == "Fazenda Primavera"
    assert new_producer.fazenda[1].nome == "Fazenda Sol Nascente"
    
    # usuário já existe
    duplicate_producer = Produtor(
        nome="Pedro da Silva",
        cpf_cnpj="93231382076",
        telefone="11985768364",
        email="pedro.silva@teste.com.br",
        senha="123Abc!!",
        tipo="comum",
        ativo=True
    )
    db.add(duplicate_producer)
    with pytest.raises(IntegrityError):
        db.commit()

    db.rollback()
    
def test_get_producers(db, producers_in_db):
    """Testa a obtenção de produtores."""
    producers = db.query(Produtor).all()
    assert len(producers) == 3
    
def test_get_producer_by_name(db, producers_in_db):
    """Testa a obtenção de um produtor pelo nome."""
    producer = db.query(Produtor).filter(Produtor.nome == "Bruno Lima").first()
    assert producer is not None
    
def test_update_producer(db, producers_in_db):
    """Testa a atualização de um produtor."""
    producer = db.query(Produtor).filter(Produtor.nome == "Bruno Lima").first()
    producer.ativo = False
    db.commit()
    producer = db.query(Produtor).filter(Produtor.nome == "Bruno Lima").first()
    assert producer.ativo is False
    
def test_delete_producer(db, producers_in_db, farms_in_db):
    """Testa a exclusão de um produtor."""
    producer = db.query(Produtor).filter(Produtor.nome == "Bruno Lima").first()
    db.delete(producer)
    db.commit()
    producer = db.query(Produtor).filter(Produtor.nome == "Bruno Lima").first()
    assert producer is None

    # produtor está associado a fazenda, a faszenda não deve ser excluida
    producer_with_farm = db.query(Produtor).filter(Produtor.id == 2).first()
    farms = db.query(Fazenda).all()
    expected_len = len(farms)
    farms[0].fazenda = producer_with_farm
    farms[1].fazenda = producer_with_farm
    db.delete(producer_with_farm)
    db.commit()
    farms = db.query(Fazenda).all()
    assert len(farms) == expected_len