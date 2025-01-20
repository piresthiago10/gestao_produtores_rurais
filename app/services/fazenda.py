class Fazenda:
    """Classe Fazenda."""

    def __init__(self, model, db):
        """Inicia a classe com suas configurações."""
        self.model = model
        self.db = db
        
    def _validate_areas(self, agricultural_area: int, vegetation_area: int, total_area: int):
        """Valida se a soma das áreas agricultável e de vegetação não excede a área total."""
        if agricultural_area + vegetation_area > total_area:
            raise ValueError(
                "A soma das áreas agricultável e de vegetação não "
                + "pode exceder a área total da fazenda."
            )
        
    async def create(self, data: dict):
        """Cria uma nova safra."""
        self._validate_areas(data["area_agricultavel"], data["area_vegetacao"], data["area_total"])
        result = await self.db.create(self.model, data)
        new_data = await self.db.get_by_id(self.model, result.id)
        return new_data
    
    async def get_by_id(self, id: int):
        """Obtem uma safra pelo ID."""
        result = await self.db.get_by_id(self.model, id)
        return result
    
    async def get_all(self):
        """Obtem todas as fazendas."""
        result = await self.db.get_all(self.model)
        return result

    async def update(self, id: int, data: dict):
        """Atualiza uma safra."""
        self._validate_areas(data["area_agricultavel"], data["area_vegetacao"], data["area_total"])
        result = await self.db.update(self.model, id, data)
        return result
    
    async def delete(self, id: int):
        """Exclui uma safra."""
        result = await self.db.delete(self.model, id)
        return result
    
    async def soft_delete(self, id: int):
        """Inativa uma safra."""
        result = await self.db.soft_delete(self.model, id)
        return result
    
    async def get_dashboard_data(self, crop_model):
        """Retorna os dados para o dashboard."""
        total_farms = await self.db.get_total_farms(self.model)
        total_area = await self.db.get_total_area(self.model)
        farms_by_state = await self.db.get_farms_by_state(self.model)
        farms_by_culture = await self.db.get_farms_by_culture(self.model, crop_model)
        farms_by_soil_use = await self.db.get_farms_by_soil_use(self.model)
        result = {
            "total_farms": total_farms,
            "total_area": total_area,
            "farms_by_state": farms_by_state,
            "farms_by_culture": farms_by_culture,
            "farms_by_soil_use": farms_by_soil_use}
        return result