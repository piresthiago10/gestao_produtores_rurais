import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database.database import DataBase
from app.database.crud_usuario import CRUD_Usuario
from app.models.models import Usuario
from app.services.usuario import Usuario as UsuarioService
from app.schemas.usuario import CreateUpdateUsuario

from app.config import DATABASE

data_base = DataBase(DATABASE)

logger = logging.getLogger(__name__)


async def get_db():
    """Retorna a sessão de conexão com o banco de dados."""
    async for session in data_base.get_db():
        yield session


router = APIRouter()


@router.post("/", tags=["Usuario"])
async def create_user(request: Request, data: CreateUpdateUsuario, db=Depends(get_db)):
    """Cria um novo usuario."""
    crud = CRUD_Usuario(db)
    usuario_service = UsuarioService(Usuario, crud)
    try:
        response = await usuario_service.create(data.model_dump())
        response_no_password = jsonable_encoder(response)
        del response_no_password["senha_hash"]
        logger.info(f"Usuário criado em {request.url.path}")
        return JSONResponse(
            status_code=201, content=jsonable_encoder(response_no_password)
        )
    except Exception as e:
        logger.error(f"Erro ao criar usuário em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", tags=["Usuario"])
async def get_users(request: Request, db=Depends(get_db)):
    """Busca todos os usuarios."""
    crud = CRUD_Usuario(db)
    usuario_service = UsuarioService(Usuario, crud)
    try:
        response = await usuario_service.get_all()
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", tags=["Usuario"])
async def get_user_by_id(request: Request, id: int, db=Depends(get_db)):
    """Busca um usuario pelo id."""
    crud = CRUD_Usuario(db)
    usuario_service = UsuarioService(Usuario, crud)
    try:
        response = await usuario_service.get_by_id(id)
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cpf_cnpj/{cpf_cnpj}", tags=["Usuario"])
async def get_user_by_cpf_cnpj(request: Request, cpf_cnpj: str, db=Depends(get_db)):
    """Busca um usuario pelo cpf_cnpj."""
    crud = CRUD_Usuario(db)
    usuario_service = UsuarioService(Usuario, crud)
    try:
        response = await usuario_service.get_by_cpf_cnpj(cpf_cnpj)
        logger.info(f"Dados buscados em {request.url.path}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response))
    except Exception as e:
        logger.error(f"Dados buscados em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", tags=["Usuario"])
async def update_user(
    request: Request, id: int, data: CreateUpdateUsuario, db=Depends(get_db)
):
    """Atualiza um usuario."""
    crud = CRUD_Usuario(db)
    usuario_service = UsuarioService(Usuario, crud)
    try:
        response = await usuario_service.update(id, data)
        response_no_password = jsonable_encoder(response)
        del response_no_password["senha_hash"]
        logger.info(f"Usuário atualizado em {request.url.path}")
        return JSONResponse(
            status_code=200, content=jsonable_encoder(response_no_password)
        )
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", tags=["Usuario"])
async def delete_user(request: Request, id: int, db=Depends(get_db)):
    """Exclui um usuario."""
    crud = CRUD_Usuario(db)
    usuario_service = UsuarioService(Usuario, crud)
    try:
        response = await usuario_service.delete(id)
        logger.info(f"Usuário excluido em {request.url.path}")
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        logger.error(f"Erro ao excluir usuário em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/ativo/{id}", tags=["Usuario"])
async def soft_delete_user(request: Request, id: int, db=Depends(get_db)):
    """Desativa um usuario."""
    crud = CRUD_Usuario(db)
    usuario_service = UsuarioService(Usuario, crud)
    try:
        response = await usuario_service.soft_delete(id)
        logger.info(f"Usuário desativado em {request.url.path}")
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        logger.error(f"Erro ao desativar usuário em {request.url.path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
