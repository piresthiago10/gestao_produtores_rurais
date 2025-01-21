import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from app.database.database import DataBase
from app.database.crud_fazenda import CRUD_Fazenda
from app.models.models import Fazenda, Safra
from app.services.fazenda import Fazenda as FazendaService
from app.schemas.fazenda import CreateUpdateFazenda, FazendaResponse

from app.config import DATABASE

data_base = DataBase(DATABASE)

logger = logging.getLogger(__name__)


async def get_db():
    """Retorna a sessão de conexão com o banco de dados."""
    async for session in data_base.get_db():
        yield session


router = APIRouter()


@router.post("/", tags=["Fazenda"])
async def create_fazenda(
    request: Request, data: CreateUpdateFazenda, db=Depends(get_db)
):
    """Cria uma nova fazenda."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.create(data.model_dump())
        logger.info(f"Fazenda criada em {request.url.path}")
        return JSONResponse(status_code=201, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao criar fazenda em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[FazendaResponse], tags=["Fazenda"])
async def get_fazenda(request: Request, db=Depends(get_db)):
    """Busca todas as fazenda."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.get_all()
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=FazendaResponse, tags=["Fazenda"])
async def get_fazenda_by_id(request: Request, id: int, db=Depends(get_db)):
    """Busca uma fazenda pelo id."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.get_by_id(id)
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", tags=["Fazenda"])
async def update_fazenda(
    request: Request, id: int, data: CreateUpdateFazenda, db=Depends(get_db)
):
    """Atualiza uma fazenda."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.update(id, data.model_dump())
        logger.info(f"Fazenda atualizada em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao atualizar fazenda em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", tags=["Fazenda"])
async def delete_fazenda(request: Request, id: int, db=Depends(get_db)):
    """Exclui uma fazenda."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.delete(id)
        logger.info(f"Fazenda excluida em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao excluir fazenda em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/ativo/{id}", tags=["Fazenda"])
async def soft_delete_fazenda(request: Request, id: int, db=Depends(get_db)):
    """Desativa uma fazenda."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.soft_delete(id)
        logger.info(f"Fazenda desativada em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Erro ao desativar fazenda em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/dashboard/data", tags=["Fazenda"])
async def get_fazenda_dashboard(request: Request, db=Depends(get_db)):
    """Busca dados para o dashboard."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.get_dashboard_data(Safra)
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/handle_crop_in_farm/add/{farm_id}/{crop_id}",
    response_model=FazendaResponse,
    tags=["Fazenda"],
)
async def handle_crop_in_farm_add(
    request: Request, crop_id: int, farm_id: int, db=Depends(get_db)
):
    """Adiciona uma cultura a uma fazenda."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.handle_crop_in_farm(
            Safra, farm_id, crop_id, True
        )
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/handle_crop_in_farm/remove/{farm_id}/{crop_id}",
    response_model=FazendaResponse,
    tags=["Fazenda"],
)
async def handle_crop_in_farm_remove(
    request: Request, crop_id: int, farm_id: int, db=Depends(get_db)
):
    """Remove uma cultura da fazenda."""
    crud = CRUD_Fazenda(db)
    fazenda_service = FazendaService(Fazenda, crud)
    try:
        response = await fazenda_service.handle_crop_in_farm(
            Safra, farm_id, crop_id, False
        )
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
