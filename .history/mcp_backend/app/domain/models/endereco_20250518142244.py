from pydantic import BaseModel
from models.estado import Estado  # Enum flexível com tratamento de entrada

class Endereco(BaseModel):
    rua: str
    cidade: str
    estado: Estado