from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base
import bcrypt

class Usuario(Base):
    """Tabela Usuários."""
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=False)
    telefone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, unique=False, nullable=False)
    tipo = Column(String, unique=False, nullable=False)
    ativo = Column(Boolean, unique=False, nullable=False)

    def __repr__(self):
        """Representação do usuário."""
        return f"<Usuario(id={self.id}, nome={self.nome}, email={self.email}, tipo={self.tipo})>"
    
    @property
    def senha(self):
        """Senha não pode ser acessada diretamente."""
        raise AttributeError("A senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, senha_sem_hash: str):
        """Define o hash da senha usando bcrypt."""
        self.senha_hash = bcrypt.hashpw(
            senha_sem_hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, senha_sem_hash: str) -> bool:
        """Verifica se a senha clara corresponde ao hash armazenado."""
        return bcrypt.checkpw(senha_sem_hash.encode('utf-8'), self.senha_hash.encode('utf-8'))