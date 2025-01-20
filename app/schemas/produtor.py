from pydantic import BaseModel, conint, constr, Field, field_validator, EmailStr
from app.utils.cpf_validator import validate_cpf
from app.utils.cnpj_validator import validate_cnpj
from typing import List, Literal, Optional
import re

class CreateUpdateProdutor(BaseModel):
    """Schema para criação ou atualização de um produtor."""
    nome: str = Field(description="Nome", example="Pedro da Silva", max_length=100)
    cpf_cnpj: str = Field(description="CPF ou CNPJ", example="123.456.789-00")
    telefone: str = Field(description="Telefone", example="11999999999")
    email: EmailStr = Field(description="Email", example="pedro.silva@teste.com.br")
    senha: str = Field(description="Senha", example="123Abc!!")
    tipo: Literal["comum"] = Field(example="comum", description="O tipo de produtor.")
    ativo: bool = Field(example=True, description="Se o produtor esta ativo.")

    @field_validator("cpf_cnpj")
    def validate_cpf_or_cnpj(cls, cpf_cnpj: str) -> str:
        is_valid_cpf = validate_cpf(cpf_cnpj)
        is_valid_cnpj = validate_cnpj(cpf_cnpj)
        if is_valid_cnpj or is_valid_cpf:
            return cpf_cnpj
        raise ValueError("CPF/CNPJ inválido")
    
    @field_validator("nome")
    def name_validator(cls, nome):
        """Validate nome."""
        data = nome.strip()
        if len(data.split(" ")) < 2 or len(data) > 100:
            raise ValueError("Nome inválido")
        return data
    
    @field_validator("telefone")
    def validate_telefone(cls, telefone: str) -> str:
        pattern = re.compile(r"^(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}$")
        if not pattern.match(telefone):
            raise ValueError("Telefone inválido. Formato: (99) 99999-9999 ou 99999-9999")
        
        telefone = re.sub(r"[()\s-]", "", telefone)
        return telefone