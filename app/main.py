from fastapi import FastAPI
from app.logs.conflogging import setup_logging
from app.routers import (
    usuario as usuario_router,
    produtor as produtor_router,
    safra as safra_router,
    fazenda as fazenda_router,
)
from fastapi.responses import ORJSONResponse

setup_logging()

app = FastAPI(
    title="Gestão de Produtores Rurais",
    description="API para gerenciamento de produtores rurais.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
)

app.include_router(usuario_router.router, prefix="/usuario", tags=["Usuario"])
app.include_router(produtor_router.router, prefix="/produtor", tags=["Produtor"])
app.include_router(safra_router.router, prefix="/safra", tags=["Safra"])
app.include_router(fazenda_router.router, prefix="/fazenda", tags=["Fazenda"])


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à minha API!"}
