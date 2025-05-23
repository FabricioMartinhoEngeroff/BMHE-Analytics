from sqlalchemy.orm import mapped_as_dataclass, Mapped, mapped_column
from sqlalchemy import String
from mcp_backend.app.domain.base import registry  # seu registry central

class Endereco(Base):
    __tablename__ = "enderecos"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    rua: Mapped[str]    = mapped_column(String, nullable=False)
    numero: Mapped[str] = mapped_column(String, nullable=False)
    cidade: Mapped[str] = mapped_column(String, nullable=False)
    estado: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship("User", back_populates="endereco")
