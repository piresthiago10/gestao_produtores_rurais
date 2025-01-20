from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from app.database.database import DataBase
from app.database.crud_produtor import CRUD_Produtor
from app.models.models import Produtor
from app.services.produtor import Produtor as ProdutorService
from app.schemas.produtor import CreateUpdateProdutor

from app.config import DATABASE

data_base = DataBase(DATABASE)
db = data_base.get_db
crud = CRUD_Produtor(db)

router = APIRouter()

@router.post("/", tags=["Produtor"])
async def create_producer(data: CreateUpdateProdutor):
    """Cria um novo produtor."""
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.create(data)
        return JSONResponse(status_code=201, content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", tags=["Produtor"])
async def get_producers(request: Request):
    """Busca todos os produtor."""
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.get_all()
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", tags=["Produtor"])
async def get_producer_by_id(id: int):
    """Busca um produtor pelo id."""
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.get_by_id(id)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cpf_cnpj/{cpf_cnpj}", tags=["Produtor"])
async def get_producer_by_cpf_cnpj(cpf_cnpj: str):
    """Busca um produtor pelo cpf_cnpj."""
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.get_by_cpf_cnpj(cpf_cnpj)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", tags=["Produtor"])
async def update_producer(id: int, data: CreateUpdateProdutor):
    """Atualiza um produtor."""
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.update(id, data)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", tags=["Produtor"])
async def delete_producer(id: int):
    """Exclui um produtor."""
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.delete(id)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/ativo/{id}", tags=["Produtor"])
async def soft_delete_producer(id: int):
    """Desativa um produtor."""
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.soft_delete(id)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
