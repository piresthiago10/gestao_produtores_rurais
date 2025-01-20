from fastapi import FastAPI
from app.database.database import DataBase, Base
from app.routers import (
    usuario as usuario_router,
    produtor as produtor_router
    )
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="Gestão de Produtores Rurais",
    description="API para gerenciamento de produtores rurais.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse
)

app.include_router(produtor_router.router, prefix="/produtor", tags=["Produtores"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à minha API!"}
