from pydantic import BaseModel, Field, constr
from .estado import Estado

class Endereco(BaseModel):
    rua:    constr(min_length=1) = Field(..., description="Nome da rua")
    numero: constr(min_length=1) = Field(..., description="Número")
    bairro: constr(min_length=1) = Field(..., description="Bairro")
    cidade: constr(min_length=1) = Field(..., description="Cidade")
    estado: Estado               = Field(..., description="UF (ex: SP, RJ)")
    cep:    constr(regex=r"^\d{5}-\d{3}$") = Field(..., description="CEP formato 00000-000")
