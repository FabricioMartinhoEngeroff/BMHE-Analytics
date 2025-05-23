from sqlalchemy import , Enum as SqlEnum
from mcp_backend.app.domain.models.base import registry
import enum
import unicodedata

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

    @classmethod
    def _missing_(cls, value: str):
        normalizado = (
            unicodedata.normalize("NFD", value)
            .encode("ascii", "ignore")
            .decode("utf-8")
            .strip()
            .upper()
        )
        for estado in cls:
            if normalizado == estado.name or normalizado == estado.value.upper():
                return estado
        raise ValueError(f"Estado inválido: {value}")
