from pydantic import BaseModel, Field, constr
from .estado import Estado

RuaType = constr(min_length=1)
NumeroType = constr(min_length=1)
BairroType = constr(min_length=1)
CidadeType = constr(min_length=1)
CepType = constr(regex=r"^\d{5}-\d{3}$")

class Endereco(BaseModel):
    rua:    RuaType    = Field(..., description="Nome da rua")
    numero: NumeroType = Field(..., description="Número")
    bairro: BairroType = Field(..., description="Bairro")
    cidade: CidadeType = Field(..., description="Cidade")
    estado: Estado     = Field(..., description="UF (ex: SP, RJ)")
    cep:    CepType    = Field(..., description="CEP formato 00000-000")
