from sqlalchemy import String, ForeignKey, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, mapped_as_dataclass
import uuid
from datetime import datetime
from mcp_backend.app.domain.models.role import Role
from mcp_backend.app.domain.models.base import registry

# Tabela intermediária users_roles (muitos para muitos)
users_roles = Table(
    "users_roles",
    registry.metadata,
    mapped_column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    mapped_column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"))
)

@mapped_as_dataclass()
class User:
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(15), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    roles: Mapped[list[Role]] = relationship(
        "Role",
        secondary=users_roles,
        lazy="joined"
    )

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
