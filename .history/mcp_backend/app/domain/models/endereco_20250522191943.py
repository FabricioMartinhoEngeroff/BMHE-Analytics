import unicodedata
from sqlalchemy import String
from sqlalchemy.orm import composite, registry
import enum

from mcp_backend.app.config.database import registry  

class Estado(enum.Enum):
    AC = "AC"; AL = "AL"; AP = "AP"; AM = "AM"; BA = "BA"
    CE = "CE"; DF = "DF"; ES = "ES"; GO = "GO"; MA = "MA"
    MT = "MT"; MS = "MS"; MG = "MG"; PA = "PA"; PB = "PB"
    PR = "PR"; PE = "PE"; PI = "PI"; RJ = "RJ"; RN = "RN"
    RS = "RS"; RO = "RO"; RR = "RR"; SC = "SC"; SP = "SP"
    SE = "SE"; TO = "TO"

    @classmethod
    def _missing_(cls, value: str):
        nf = unicodedata.normalize("NFD", value).encode("ascii","ignore").decode().upper().strip()
        for e in cls:
            if nf == e.name or nf == e.value:
                return e
        raise ValueError(f"Estado inválido: {value}")

class Endereco:
    def __init__(self, rua: str, bairro: str, cidade: str, estado: Estado, cep: str):
        self.rua    = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado.value if isinstance(estado, Estado) else estado
        self.cep    = cep

    def __composite_values__(self):
        # ordem EXATA das colunas do User
        return (self.rua, self.bairro, self.cidade, self.estado, self.cep)

    def __repr__(self):
        return f"<Endereco {self.rua}, {self.bairro}, {self.cidade}-{self.estado} [{self.cep}]>"