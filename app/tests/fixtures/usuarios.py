import pytest
from sqlalchemy.orm import Session
from app.models.usuarios import Usuario

@pytest.fixture(scope="function")
def users_in_db(db: Session):
    """Fixture para criar três usuários no banco de dados para os testes."""
    users = [
        Usuario(
            nome="Maria Oliveira",
            cpf_cnpj="98765432100",
            telefone="11912345678",
            email="maria.oliveira@teste.com.br",
            senha="Senha456!",
            tipo="admin",
            ativo=True
        ),
        Usuario(
            nome="Carlos Souza",
            cpf_cnpj="12398765400",
            telefone="11987654321",
            email="carlos.souza@teste.com.br",
            senha="Senha789!",
            tipo="comum",
            ativo=False
        ),
        Usuario(
            nome="Ana Costa",
            cpf_cnpj="56789012345",
            telefone="11923456789",
            email="ana.costa@teste.com.br",
            senha="Senha012!",
            tipo="comum",
            ativo=True
        )
    ]

    db.add_all(users)
    db.commit()
    for user in users:
        db.refresh(user)

    return users
