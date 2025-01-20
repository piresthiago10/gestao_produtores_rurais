class Safra:
    """Classe Safra."""

    def __init__(self, model, db):
        """Inicia a classe com suas configurações."""
        self.model = model
        self.db = db

    async def create(self, data: dict):
        """Cria uma nova safra."""
        result = await self.db.create(self.model, data)
        new_data = await self.db.get_by_id(self.model, result.id)
        return new_data
    
    async def get_by_id(self, id: int):
        """Retorna uma safra pelo id."""
        return await self.db.get_by_id(self.model, id)
    
    async def get_all(self):
        """Retorna todas as safra."""
        return await self.db.get_all(self.model)
    
    async def update(self, id: int, data: dict):
        """Atualiza uma safra."""
        return await self.db.update(self.model, id, data)
    
    async def delete(self, id: int):
        """Exclui uma safra."""
        return await self.db.delete(self.model, id)
    
    async def soft_delete(self, id: int):
        """Inativa uma safra."""
        return await self.db.soft_delete(self.model, id)