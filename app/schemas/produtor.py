from pydantic import BaseModel, Field, EmailStr
from typing import Literal, List


class FazendaResponse(BaseModel):
    """Schema para retorno de uma fazenda."""

    nome: str = Field(
        description="Nome", example="Fazenda 2022", min_length=10, max_length=100
    )
    area_total: int = Field(
        description="Area total da fazenda (em hectares)", example=1000
    )
    area_agricultavel: int = Field(
        description="Area agricultavel da fazenda (em hectares)", example=500
    )
    area_vegetacao: int = Field(
        description="Area vegetacao da fazenda (em hectares)", example=500
    )
    ativo: bool = Field(example=True, description="Se a fazenda estiver ativa.")

    class Config:
        orm_mode = True


class ProdutorResponse(BaseModel):
    """Schema para retorno de produtor."""

    nome: str = Field(description="Nome", example="Pedro da Silva", max_length=100)
    cpf_cnpj: str = Field(description="CPF ou CNPJ", example="17005484096")
    telefone: str = Field(description="Telefone", example="11999999999")
    email: EmailStr = Field(description="Email", example="pedro.silva@teste.com.br")
    tipo: Literal["comum", "admin"] = Field(
        example="comum", description="O tipo de usuário."
    )
    ativo: bool = Field(example=True, description="Se o usuário esta ativo.")
    fazendas: List[FazendaResponse]

    class Config:
        orm_mode = True
