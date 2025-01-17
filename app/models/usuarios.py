from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class Usuario(Base):
    """Tabela Usuários."""
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=False)
    telefone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, unique=False, nullable=False)
    tipo = Column(String, unique=False, nullable=False)
    ativo = Column(Boolean, unique=False, nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome={self.nome}, email={self.email}, tipo={self.tipo})>"