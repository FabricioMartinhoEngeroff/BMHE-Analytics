from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, mapped_as_dataclass
import uuid
from app.domain.models.base import registry  # Registro ORM compartilhado

@mapped_as_dataclass()
class Role:
    __tablename__ = "roles"
    __sa_dataclass_metadata_key__ = "sa"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )

    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )

    description: Mapped[str] = mapped_column(
        String(255), nullable=True
    )

    def __repr__(self):
        return f"<Role(name={self.name})>"
