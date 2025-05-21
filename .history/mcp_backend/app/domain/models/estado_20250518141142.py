from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, mapped_as_dataclass
from mcp_backend.app.domain.models.base import registry
import enum


# 🔠 Enum dos estados brasileiros
class Estado(str, enum.Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


@mapped_as_dataclass()
class Endereco:
    __tablename__ = "enderecos"
    __sa_dataclass_metadata_key__ = "sa"

    id: Mapped[int] = mapped_column(primary_key=True, init=False, autoincrement=True)

    rua: Mapped[str] = mapped_column(String(100), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[Estado] = mapped_column(Enum(Estado), nullable=False)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)  # Ex: "99999-999"

    def __repr__(self):
        return f"<Endereco({self.rua}, {self.bairro}, {self.cidade} - {self.estado})>"
