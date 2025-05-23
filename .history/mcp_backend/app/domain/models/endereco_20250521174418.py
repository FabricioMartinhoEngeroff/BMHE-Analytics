from sqlalchemy.orm import mapped_as_dataclass, Mapped, mapped_column
from sqlalchemy import String
from mcp_backend.app.domain.models.base import registry  # seu registry central

@mapped_as_dataclass()
class Endereco:
    __tablename__ = "enderecos"
    __sa_registry__ = registry

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    rua: Mapped[str] = mapped_column(String, nullable=False)
    numero: Mapped[str] = mapped_column(String, nullable=False)
    cidade: Mapped[str] = mapped_column(String, nullable=False)
    estado: Mapped[str] = mapped_column(String, nullable=False)  # ou Enum(Estado) se usar enum

