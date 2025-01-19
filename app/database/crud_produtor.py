from app.database.crud_usuario import CRUD_Usuario

class CRUD_Produtor(CRUD_Usuario):
    """CRUD para o modelo Produtor."""
    
    def __init__(self, db):
        """Inicia a classe com as configurações do banco de dados."""
        super().__init__(db)   
