from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Fazenda(Base):
    """Tabela Fazendas."""
    __tablename__ = "fazendas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, unique=False, nullable=False)
    estado = Column(String, unique=False, nullable=False)
    area_total = Column(Integer, unique=False, nullable=False)
    area_agricultavel = Column(Integer, unique=False, nullable=False)
    area_vegetacao = Column(Integer, unique=False, nullable=False)
    ativo = Column(Boolean, unique=False, nullable=False)
    
    produtor_id = Column(Integer, ForeignKey("produtores.id"), nullable=True)

    produtor = relationship("Produtor", back_populates="fazenda", cascade="save-update, merge")
    safra = relationship("Safra", back_populates="fazenda", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Fazenda("
            f"id={self.id}, "
            f"nome='{self.nome}', "
            f"estado='{self.estado}', "
            f"area_total={self.area_total}"
            f")>"
        )
