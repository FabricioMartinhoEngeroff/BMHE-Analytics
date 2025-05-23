from sqlalchemy.orm import mapped_as_dataclass, Mapped, mapped_column
from sqlalchemy import String
from mcp_backend.app.domain.models.base import registry  # onde está o registry central
from dataclasses import dataclass

@dataclass
class Endereco:
    __tablename__ = "enderecos"  # nome da tabela no banco (plural: boa prática)
    __sa_registry__ = registry   # registra no registry global da aplicação

    id: Mapped[int] = mapped_column(primary_key=True, init=False)  # chave primária, não precisa passar no __init__
    rua: Mapped[str] = mapped_column(String, nullable=False)
    numero: Mapped[str] = mapped_column(String, nullable=False)
    cidade: Mapped[str] = mapped_column(String, nullable=False)
    estado: Mapped[str] = mapped_column(String, nullable=False)  # se quiser, pode usar Enum(Estado) aqui depois
