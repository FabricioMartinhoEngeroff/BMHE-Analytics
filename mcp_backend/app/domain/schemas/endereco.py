from pydantic import BaseModel, Field
from app.domain.models.estado import Estado

class Endereco(BaseModel):
    rua: str = Field(..., min_length=1)
    numero: str = Field(..., min_length=1)
    cidade: str = Field(..., min_length=1)
    estado: Estado = Field(..., min_length=2)
