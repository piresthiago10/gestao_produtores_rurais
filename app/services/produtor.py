from app.services.usuario import Usuario


class Produtor(Usuario):
    def __init__(self, model, db):
        """Inicia a classe com suas configurações."""
        self.model = model
        self.db = db

    def _is_type_admin(self, data: dict):
        """Verifica se o tipo do produtor é admin."""
        if data["tipo"] == "admin":
            raise ValueError("Produtor não pode ser do tipo admin")

    async def create(self, data: dict):
        """Cria um novo produtor."""
        self._is_type_admin(data)
        result = await self.db.create(self.model, data)
        new_data = await self.db.get_by_id(self.model, result.id)
        return new_data

    async def update(self, id: int, data: dict):
        """Atualiza um produtor."""
        self._is_type_admin(data)
        return await self.db.update(self.model, id, data)

    async def handle_farm_in_producer(
        self, farm_model: object, producer_id: int, farm_id: int, is_add: bool = True
    ):
        """Adiciona uma fazenda a um produtor."""
        return await self.db.handle_farm_in_producer(
            self.model, farm_model, producer_id, farm_id, is_add
        )
