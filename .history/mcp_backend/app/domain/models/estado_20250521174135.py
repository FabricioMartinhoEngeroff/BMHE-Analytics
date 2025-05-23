from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, mapped_as_dataclass
from mcp_backend.app.domain.models.base import registry
import enum
import unicodedata
from dataclasses import dataclass

class Estado(str, Enum):
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
        """
        Método chamado automaticamente quando um valor inválido é passado à Enum.
        Ele tenta normalizar a string e encontrar o estado correspondente.
        """
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

        raise ValueError(f"Erro inválido: {value}")