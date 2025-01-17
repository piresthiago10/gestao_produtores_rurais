from app.models.usuarios import Usuario
from app.tests.fixtures.usuarios import users_in_db

def test_create_user(db):
    """Testa a criação de um novo usuário."""
    new_user = Usuario(
        nome = "Pedro da Silva",
        cpf_cnpj = "93231382076",
        telefone = "11985768364",
        email = "pedro.silva@teste.com.br",
        senha = "123Abc!!",
        tipo = "comum",
        ativo = True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # usuário foi salvo corretamenente
    assert new_user.id is not None
    assert new_user.nome == "Pedro da Silva"
    assert new_user.email == "pedro.silva@teste.com.br"
    assert new_user.tipo == "comum"
    assert new_user.ativo is True
    
def test_get_users(db, users_in_db):
    """Testa a obtenção de usuários do banco de dados."""
    users = db.query(Usuario).all()
    assert len(users) == 3
    assert users[0].nome == "Maria Oliveira"
    assert users[1].nome == "Carlos Souza"
    assert users[2].nome == "Ana Costa"
    
def test_get_user_by_name(db, users_in_db):
    """Testa a obtenção de usuários pelo nome."""
    user = db.query(Usuario).filter(Usuario.nome == "Maria Oliveira").first()
    assert user is not None
    assert user.nome == "Maria Oliveira"
    
    # Testa a obtenção de usuários pelo CPF/CNPJ
    user = db.query(Usuario).filter(Usuario.cpf_cnpj == "98765432100").first()
    assert user is not None
    assert user.nome == "Maria Oliveira"
    
    # Usuário não encontrado
    user = db.query(Usuario).filter(Usuario.cpf_cnpj == "12345678900").first()
    assert user is None
    
def test_update_user(db, users_in_db):
    """Testa a atualização de usuários."""
    user = db.query(Usuario).filter(Usuario.cpf_cnpj == "98765432100").first()
    user.ativo = False
    db.commit()
    user = db.query(Usuario).filter(Usuario.cpf_cnpj == "98765432100").first()
    assert user.ativo is False
    
def test_delete_user(db, users_in_db):
    """Testa a exclusão de usuários."""
    user = db.query(Usuario).filter(Usuario.cpf_cnpj == "98765432100").first()
    db.delete(user)
    db.commit()
    user = db.query(Usuario).filter(Usuario.cpf_cnpj == "98765432100").first()
    assert user is None
