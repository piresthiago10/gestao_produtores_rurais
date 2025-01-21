class Usuario:
    def __init__(self, model, db):
        """Inicia a classe com suas configurações."""
        self.model = model
        self.db = db

    async def create(self, data: dict):
        """Cria um novo usuario."""
        result = await self.db.create(self.model, data)
        new_data = await self.db.get_by_id(self.model, result.id)
        return new_data

    async def get_by_id(self, id: int):
        """Retorna um usuario pelo id."""
        return await self.db.get_by_id(self.model, id)

    async def get_by_cpf_cnpj(self, cpf_cnpj: str):
        """Retorna um usuario pelo cpf_cnpj."""
        return await self.db.get_by_cpf_cnpj(self.model, cpf_cnpj)

    async def get_by_email(self, email: int):
        """Retorna um usuario pelo email."""
        return await self.db.get_by_email(self.model, email)

    async def get_all(self):
        """Retorna todos os usuarios."""
        return await self.db.get_all(self.model)

    async def update(self, id: int, data: dict):
        """Atualiza um usuario."""
        return await self.db.update(self.model, id, data)

    async def delete(self, id: int):
        """Exclui um usuario."""
        return await self.db.delete(self.model, id)

    async def soft_delete(self, id: int):
        """Inativa um usuario."""
        return await self.db.soft_delete(self.model, id)
