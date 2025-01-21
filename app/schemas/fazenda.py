from pydantic import BaseModel, Field, model_validator
from typing import List


class CreateUpdateFazenda(BaseModel):
    """Schema para criação ou atualização de uma fazenda."""

    nome: str = Field(
        description="Nome", example="Fazenda 2022", min_length=10, max_length=100
    )
    cidade: str = Field(
        description="Cidade", example="Ribeirão Preto", min_length=4, max_length=100
    )
    estado: str = Field(description="Estado", example="SP", min_length=2, max_length=2)
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

    @model_validator(mode="after")
    def validate_areas(cls, self):
        if self.area_agricultavel + self.area_vegetacao > self.area_total:
            raise ValueError(
                "A soma das áreas agricultável e de vegetação não pode "
                + "exceder a área total da fazenda."
            )
        return self


class SafraResponse(BaseModel):
    """Schema para retorno de uma safra."""

    nome: str = Field(
        description="Nome", example="Safra 2022", min_length=10, max_length=100
    )
    tipo_cultura: str = Field(
        description="Tipo de cultura", example="Soja", min_length=4, max_length=100
    )
    variedade: str = Field(
        description="Variedade", example="Orgânico", min_length=4, max_length=100
    )
    ano_plantio: int = Field(description="Ano de plantio", example=2022)
    ano_colheita: int = Field(description="Ano de colheita", example=2023)
    produtividade_tonelada: float = Field(
        description="Produtividade em toneladas", example=50.5
    )
    ativo: bool = Field(example=True, description="Se a safra estiver ativa.")

    class Config:
        orm_mode = True


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
    safras: List[SafraResponse]

    class Config:
        orm_mode = True
