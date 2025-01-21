import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.database.database import DataBase
from app.database.crud_produtor import CRUD_Produtor
from app.models.models import Produtor, Fazenda
from app.services.produtor import Produtor as ProdutorService
from app.schemas.usuario import CreateUpdateUsuario as CreateUpdateProdutor
from app.schemas.produtor import ProdutorResponse
from typing import List

from app.config import DATABASE

data_base = DataBase(DATABASE)

logger = logging.getLogger(__name__)


async def get_db():
    """Retorna a sessão de conexão com o banco de dados."""
    async for session in data_base.get_db():
        yield session


router = APIRouter()


@router.post("/", tags=["Produtor"])
async def create_producer(
    request: Request, data: CreateUpdateProdutor, db=Depends(get_db)
):
    """Cria um novo produtor."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.create(data.model_dump())
        logger.info(f"Produtor criado em {request.url.path}")
        return JSONResponse(status_code=201, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao criar produtor em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProdutorResponse], tags=["Produtor"])
async def get_producers(request: Request, db=Depends(get_db)):
    """Busca todos os produtor."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.get_all()
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=ProdutorResponse, tags=["Produtor"])
async def get_producer_by_id(request: Request, id: int, db=Depends(get_db)):
    """Busca um produtor pelo id."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.get_by_id(id)
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cpf_cnpj/{cpf_cnpj}", response_model=ProdutorResponse, tags=["Produtor"])
async def get_producer_by_cpf_cnpj(request: Request, cpf_cnpj: str, db=Depends(get_db)):
    """Busca um produtor pelo cpf_cnpj."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.get_by_cpf_cnpj(cpf_cnpj)
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", tags=["Produtor"])
async def update_producer(
    request: Request, id: int, data: CreateUpdateProdutor, db=Depends(get_db)
):
    """Atualiza um produtor."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.update(id, data.model_dump())
        logger.info(f"Produtor atualizado em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao atualizar produtor em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", tags=["Produtor"])
async def delete_producer(request: Request, id: int, db=Depends(get_db)):
    """Exclui um produtor."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.delete(id)
        logger.info(f"Produtor excluido em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao excluir produtor em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/ativo/{id}", tags=["Produtor"])
async def soft_delete_producer(request: Request, id: int, db=Depends(get_db)):
    """Desativa um produtor."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.soft_delete(id)
        logger.info(f"Produtor desativado em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao desativar produtor em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# handle_farm_in_producer
@router.put("/handle_farm_in_producer/add/{producer_id}/{farm_id}", tags=["Produtor"])
async def handle_farm_in_producer_add(
    request: Request, producer_id: int, farm_id: int, db=Depends(get_db)
):
    """Adiciona uma fazenda a um produtor."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.handle_farm_in_producer(
            Fazenda, producer_id, farm_id
        )
        logger.info(f"Fazenda adicionada ao produtor em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(
            f"Erro ao adicionar fazenda ao produtor em {request.url.path}: {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/handle_farm_in_producer/remove/{producer_id}/{farm_id}", tags=["Produtor"]
)
async def handle_farm_in_producer_add(
    request: Request, producer_id: int, farm_id: int, db=Depends(get_db)
):
    """Remova uma fazenda de um produtor."""
    crud = CRUD_Produtor(db)
    produtor_service = ProdutorService(Produtor, crud)
    try:
        response = await produtor_service.handle_farm_in_producer(
            Fazenda, producer_id, farm_id, False
        )
        logger.info(f"Fazenda removida do produtor em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao remover fazenda do produtor em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
