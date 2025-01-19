import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.models import Usuario
from app.tests.fixtures.usuario import users_in_db

@pytest.mark.asyncio
async def test_create_user(get_db):
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
    
    get_db.add(new_user)
    await get_db.commit()
    await get_db.refresh(new_user)

    # usuário foi salvo corretamenente
    assert new_user.id is not None
    assert new_user.nome == "Pedro da Silva"
    assert new_user.email == "pedro.silva@teste.com.br"
    assert new_user.tipo == "comum"
    assert new_user.ativo is True
    
    # usuário já existe
    duplicate_user = Usuario(
        nome="Pedro da Silva",
        cpf_cnpj="93231382076",
        telefone="11985768364",
        email="pedro.silva@teste.com.br",
        senha="123Abc!!",
        tipo="comum",
        ativo=True
    )
    get_db.add(duplicate_user)
    with pytest.raises(IntegrityError):
        await get_db.commit()

    await get_db.rollback()

@pytest.mark.asyncio
async def test_verify_password(get_db):
    """Testa a verificação de senha."""
    new_user = Usuario(
        nome = "Pedro da Silva",
        cpf_cnpj = "93231382076",
        telefone = "11985768364",
        email = "pedro.silva@teste.com.br",
        senha = "123Abc!!",
        tipo = "comum",
        ativo = True
    )

    get_db.add(new_user)
    await get_db.commit()
    await get_db.refresh(new_user)

    # não permite acesso diretamente da senha
    with pytest.raises(AttributeError) as excinfo:
        new_user.senha
    excinfo.match("A senha não pode ser acessada diretamente.")

    assert new_user.verify_password("123Abc!!") is True

@pytest.mark.asyncio
async def test_get_users(get_db, users_in_db):
    """Testa a obtenção de usuários do banco de dados."""
    result = await get_db.execute(select(Usuario))
    users = result.scalars().all()
    assert len(users) == 3
    assert users[0].nome == "Maria Oliveira"
    assert users[1].nome == "Carlos Souza"
    assert users[2].nome == "Ana Costa"
    
@pytest.mark.asyncio
async def test_get_user_by_name(get_db, users_in_db):
    """Testa a obtenção de usuários pelo nome."""
    result = await get_db.execute(select(Usuario).where(Usuario.nome == "Maria Oliveira"))
    user = result.scalars().first()
    assert user is not None
    assert user.nome == "Maria Oliveira"
    
    # Testa a obtenção de usuários pelo CPF/CNPJ
    result = await get_db.execute(select(Usuario).where(Usuario.cpf_cnpj == "98765432100"))
    user = result.scalars().first()
    assert user is not None
    assert user.nome == "Maria Oliveira"
    
    # Usuário não encontrado
    result = await get_db.execute(select(Usuario).where(Usuario.cpf_cnpj == "12345678900"))
    user = result.scalars().first()
    assert user is None
    
@pytest.mark.asyncio
async def test_update_user(get_db, users_in_db):
    """Testa a atualização de usuários."""
    result = await get_db.execute(select(Usuario).where(Usuario.cpf_cnpj == "98765432100"))
    user = result.scalars().first()
    user.ativo = False
    await get_db.commit()
    result = await get_db.execute(select(Usuario).where(Usuario.cpf_cnpj == "98765432100"))
    user = result.scalars().first()
    assert user.ativo is False
    
@pytest.mark.asyncio
async def test_delete_user(get_db, users_in_db):
    """Testa a exclusão de usuários."""
    result = await get_db.execute(select(Usuario).where(Usuario.cpf_cnpj == "98765432100"))
    user = result.scalars().first()
    await get_db.delete(user)
    await get_db.commit()
    result = await get_db.execute(select(Usuario).where(Usuario.cpf_cnpj == "98765432100"))
    user = result.scalars().first()
    assert user is None
