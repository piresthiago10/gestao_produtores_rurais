import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.database.database import DataBase
from app.database.crud_safra import CRUD_Safra
from app.models.models import Safra
from app.services.safra import Safra as SafraService
from app.schemas.safra import CreateUpdateSafra

from app.config import DATABASE

data_base = DataBase(DATABASE)

logger = logging.getLogger(__name__)


async def get_db():
    """Retorna a sessão de conexão com o banco de dados."""
    async for session in data_base.get_db():
        yield session


router = APIRouter()


@router.post("/", tags=["Safra"])
async def create_safra(request: Request, data: CreateUpdateSafra, db=Depends(get_db)):
    """Cria uma nova safra."""
    crud = CRUD_Safra(db)
    safra_service = SafraService(Safra, crud)
    try:
        response = await safra_service.create(data.model_dump())
        logger.info(f"Safra criada em {request.url.path}")
        return JSONResponse(status_code=201, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao criar safra em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", tags=["Safra"])
async def get_safra(request: Request, db=Depends(get_db)):
    """Busca todas as safra."""
    crud = CRUD_Safra(db)
    safra_service = SafraService(Safra, crud)
    try:
        response = await safra_service.get_all()
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", tags=["Safra"])
async def get_safra_by_id(request: Request, id: int, db=Depends(get_db)):
    """Busca uma safra pelo id."""
    crud = CRUD_Safra(db)
    safra_service = SafraService(Safra, crud)
    try:
        response = await safra_service.get_by_id(id)
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", tags=["Safra"])
async def update_safra(
    request: Request, id: int, data: CreateUpdateSafra, db=Depends(get_db)
):
    """Atualiza uma safra."""
    crud = CRUD_Safra(db)
    safra_service = SafraService(Safra, crud)
    try:
        response = await safra_service.update(id, data)
        logger.info(f"Safra atualizada em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao atualizar safra em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", tags=["Safra"])
async def delete_safra(request: Request, id: int, db=Depends(get_db)):
    """Exclui uma safra."""
    crud = CRUD_Safra(db)
    safra_service = SafraService(Safra, crud)
    try:
        response = await safra_service.delete(id)
        logger.info(f"Safra excluida em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao excluir safra em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/ativo/{id}", tags=["Safra"])
async def soft_delete_safra(request: Request, id: int, db=Depends(get_db)):
    """Desativa uma safra."""
    crud = CRUD_Safra(db)
    safra_service = SafraService(Safra, crud)
    try:
        response = await safra_service.soft_delete(id)
        logger.info(f"Safra desativada em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao desativar safra em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
