from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Safra(Base):
    """Tabela Safras."""
    __tablename__ = "safras"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    tipo_cultura = Column(String, unique=False, nullable=False)
    variedade = Column(String, unique=False, nullable=False)
    ano_plantio = Column(Integer, unique=False, nullable=False)
    ano_colheita = Column(Integer, unique=False, nullable=False)
    produtividade_tonelada = Column(Float, unique=False, nullable=False)
    ativo = Column(Boolean, unique=False, nullable=False)

    fazenda_id = Column(Integer, ForeignKey("fazendas.id"), nullable=True)

    fazenda = relationship("Fazenda", back_populates="safra", cascade="save-update, merge")

    def __repr__(self):
        return (
            f"<Safra("
            f"id={self.id}, "
            f"nome='{self.nome}', "
            f"tipo_cultura='{self.tipo_cultura}', "
            f"ano_colheita={self.ano_colheita}"
            f")>"
        )
