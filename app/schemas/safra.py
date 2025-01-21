from pydantic import BaseModel, Field, model_validator


class CreateUpdateSafra(BaseModel):
    """Schema para criação ou atualização de uma Safra."""

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

    @model_validator(mode="after")
    def validate_anos(cls, values):
        if values.ano_plantio > values.ano_colheita:
            raise ValueError(
                "O ano de plantio não pode ser maior que o ano de colheita."
            )
        return values
