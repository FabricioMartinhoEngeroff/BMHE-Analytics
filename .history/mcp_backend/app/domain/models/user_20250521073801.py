# user.py
from sqlalchemy import Column, String, ForeignKey, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from mcp_backend.app.domain.models.role import Role
from mcp_backend.app.domain.models.base import registry

Base = registry.generate_base()

# Correção: use Column aqui, não mapped_column
users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"))
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(15), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    roles: Mapped[list[Role]] = relationship("Role", secondary=users_roles, lazy="joined")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
