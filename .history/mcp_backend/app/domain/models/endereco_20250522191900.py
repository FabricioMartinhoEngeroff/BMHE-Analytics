import unicodedata
import enum

class Estado(enum.Enum):
    AC = "AC"
    AL = "AL"
    # …

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