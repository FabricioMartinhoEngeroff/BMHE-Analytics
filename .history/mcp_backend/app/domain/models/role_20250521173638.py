import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from mcp_backend.app.config.database import Base  # usa o Base final definido via registry.generate_base()

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"<Role(name={self.name})>"
