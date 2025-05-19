from sqlalchemy.orm import mapped_as_dataclass, Mapped, mapped_column
from sqlalchemy import String, Enum as SqlEnum
from app.domain.models.base import registry
from app.domain.models.estado import Estado

@mapped_as_dataclass()
class Endereco:
    __tablename__ = "enderecos"
    __sa_registry__ = registry

    rua: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[Estado] = mapped_column(SqlEnum(Estado), nullable=False)
