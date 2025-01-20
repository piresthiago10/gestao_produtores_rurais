from sqlalchemy import select
from app.database.database import Base

class CRUD:
    """Cria um crud para o banco de dados."""
    def __init__(self, db):
        """Inicia a classe com as configurações do banco de dados."""
        self.db = db
        
    async def create(self, model: Base, data: dict) -> object:
        """Insere um novo dado no banco de dados."""
        new_data = model(**data)
        try:
            self.db.add(new_data)
            await self.db.commit()
            await self.db.refresh(new_data)
        except Exception as e:
            await self.db.rollback()
            raise e
        return new_data
    
    async def get_by_id(self, model: Base, id: int) -> object:
        """Retorna um dado do banco de dados pelo id."""
        try:
            result = await self.db.execute(select(model).where(model.id == id))
        except Exception as e:
            raise e
        return result.scalars().first()
    
    async def get_all(self, model: Base) -> list:
        """Retorna todos os dados do banco de dados."""
        try:
            result = await self.db.execute(select(model))
        except Exception as e:
            raise e
        return result.scalars().all()
    
    async def update(self, model: Base, id: int, data: dict) -> object:
        """Atualiza um dado do banco de dados."""
        result = await self.db.execute(select(model).where(model.id == id))
        db_data = result.scalars().first()
        if not db_data:
            raise Exception("Dado nao encontrado")
        for key, value in data.items():
            setattr(db_data, key, value)
            
        try:
            await self.db.commit()
            await self.db.refresh(db_data)
        except Exception as e:
            await self.db.rollback()
            raise e
        return db_data
    
    async def soft_delete(self, model: Base, id: int) -> None:
        """Inativa um dado do banco de dados."""
        result = await self.db.execute(select(model).where(model.id == id))
        db_data = result.scalars().first()
        if not db_data:
            raise Exception("Dado nao encontrado")
        db_data.ativo = False
        
        try:
            await self.db.commit()
            await self.db.refresh(db_data)
        except Exception as e:
            await self.db.rollback()
            raise e      
        return True
        
    async def delete(self, model: Base, id: int) -> None:
        """Exclui um dado do banco de dados."""
        result = await self.db.execute(select(model).where(model.id == id))
        db_data = result.scalars().first()
        if not db_data:
            raise Exception("Dado nao encontrado")
        
        try:
            await self.db.delete(db_data)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e       
        return True
