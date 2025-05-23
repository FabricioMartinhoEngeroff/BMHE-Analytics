from pydantic import BaseModel, Field


class Endereco(BaseModel):
    rua: str = Field(..., min_length=1)
    numero: str = Field(..., min_length=1)
    cidade: str = Field(..., min_length=1)
    estado: Estado = Field(..., description="Sigla do estado, ex: 'SP'")
    cep: str = Field(
        ...,
        pattern=r"^\d{5}-\d{3}$",
        description="CEP no formato 99999-999"
    )
