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
        """normalize e compara sem acentuação / case-insensitive"""
        nf = unicodedata.normalize("NFD", value).encode("ascii","ignore").decode().upper().strip()
        for e in cls:
            if nf == e.name or nf == e.value:
                return e
        raise ValueError(f"Estado inválido: {value}")

@mapped_as_dataclass()
class EnderecoModel:
    __tablename__   = "enderecos"
    __sa_registry__ = registry

    id:      Mapped[int]    = mapped_column(init=False, primary_key=True)
    rua:     Mapped[str]    = mapped_column(String, nullable=False)
    numero:  Mapped[str]    = mapped_column(String, nullable=False)
    cidade:  Mapped[str]    = mapped_column(String, nullable=False)
    estado:  Mapped[str]    = mapped_column(String(2), nullable=False)
    cep:     Mapped[str]    = mapped_column(String(9), nullable=False)

    def __composite_values__(self):
        # A ordem aqui deve bater com as colunas abaixo
        return (self.rua, self.bairro, self.cidade, self.estado, self.cep)

    def __repr__(self):
        return f"<Endereco {self.rua}, {self.bairro}, {self.cidade}-{self.estado} [{self.cep}]>"
