from sqlalchemy import Column, Integer
from app.models.usuario import Usuario
from sqlalchemy.orm import relationship

class Produtor(Usuario):
    __tablename__ = "produtores"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    __mapper_args__ = {
        'inherit_condition': Usuario.id == id
    }

    fazenda = relationship("Fazenda", back_populates="produtor", cascade="save-update, merge")
