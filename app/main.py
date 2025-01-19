from fastapi import FastAPI
from app.database.database import DataBase, Base
from app.routers import usuario

app = FastAPI(
    title="Gestão de Produtores Rurais",
    description="API para gerenciamento de produtores rurais.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# app.include_router(usuario.router, prefix="/usuarios", tags=["Usuários"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à minha API!"}
