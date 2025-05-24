# mcp_backend/app/domain/models/user.py
import uuid
from datetime import datetime
from sqlalchemy import String, func, Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite
from mcp_backend.app.config.database import Base
from mcp_backend.app.domain.models.role import Role
from mcp_backend.app.domain.models.endereco import Endereco

# Associação M-N entre usuários e roles — usa Column e NÃO mapped_column aqui!
users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(15), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # colunas individuais do endereço
    rua: Mapped[str] = mapped_column(String(255), nullable=False)
    bairro: Mapped[str] = mapped_column(String(255), nullable=False)
    cidade: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)

    endereco: Mapped[Endereco] = composite(
        Endereco,
        rua, bairro, cidade, estado, cep
    )

    roles: Mapped[list[Role]] = relationship(
        "Role",
        secondary=users_roles,
        lazy="joined"
    )

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
