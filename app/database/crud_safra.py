from app.database.crud import CRUD


class CRUD_Safra(CRUD):
    """CRUD para o modelo Safra."""

    def __init__(self, db):
        """Inicia a classe com as configurações do banco de dados."""
        super().__init__(db)
