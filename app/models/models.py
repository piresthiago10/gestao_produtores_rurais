import bcrypt
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship
from app.database.database import Base


class Usuario(Base):
    """Tabela Usuários."""

    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cpf_cnpj: Mapped[str] = mapped_column(unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(nullable=False)
    tipo: Mapped[str] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False)

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
            senha_sem_hash.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, senha_sem_hash: str) -> bool:
        """Verifica se a senha clara corresponde ao hash armazenado."""
        return bcrypt.checkpw(
            senha_sem_hash.encode("utf-8"), self.senha_hash.encode("utf-8")
        )


class Produtor(Usuario):
    """Classe para o modelo Produtor."""

    __tablename__ = "produtores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    fazenda: Mapped[list["Fazenda"]] = relationship(
        "Fazenda",
        back_populates="produtor",
        cascade="save-update, merge",
        lazy="selectin",
    )
    __mapper_args__ = {
        "polymorphic_identity": "produtor",
        "inherit_condition": Usuario.id == Usuario.id,
    }


class Safra(Base):
    """Tabela Safras."""

    __tablename__ = "safras"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    tipo_cultura: Mapped[str] = mapped_column(nullable=False)
    variedade: Mapped[str] = mapped_column(nullable=False)
    ano_plantio: Mapped[int] = mapped_column(nullable=False)
    ano_colheita: Mapped[int] = mapped_column(nullable=False)
    produtividade_tonelada: Mapped[float] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False)

    fazenda_id: Mapped[int] = mapped_column(ForeignKey("fazendas.id"), nullable=True)

    fazenda: Mapped[list["Fazenda"]] = relationship(
        "Fazenda",
        back_populates="safra",
    )

    def __repr__(self):
        return (
            f"<Safra("
            f"id={self.id}, "
            f"nome='{self.nome}', "
            f"tipo_cultura='{self.tipo_cultura}', "
            f"ano_colheita={self.ano_colheita}"
            f")>"
        )


class Fazenda(Base):
    """Modelo para a tabela Fazendas."""

    __tablename__ = "fazendas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cidade: Mapped[str] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(nullable=False)
    area_total: Mapped[int] = mapped_column(nullable=False)
    area_agricultavel: Mapped[int] = mapped_column(nullable=False)
    area_vegetacao: Mapped[int] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False)

    produtor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("produtores.id"), nullable=True
    )

    produtor: Mapped[Optional["Produtor"]] = relationship(
        "Produtor", back_populates="fazenda", cascade="save-update, merge"
    )

    safra: Mapped[List["Safra"]] = relationship(
        "Safra", back_populates="fazenda", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Fazenda("
            f"id={self.id}, "
            f"nome='{self.nome}', "
            f"estado='{self.estado}', "
            f"area_total={self.area_total}"
            f")>"
        )
