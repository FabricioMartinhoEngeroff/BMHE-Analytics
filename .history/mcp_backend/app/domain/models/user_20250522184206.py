# mcp_backend/app/domain/models/user.py
import uuid
from sqlalchemy import String, Column, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite
from sqlalchemy import Table, ForeignKey
from mcp_backend.app.config.database import Base
from .endereco import Endereco, Estado

# Association table for many-to-many relationship between users and roles
users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", PG_UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("role_id", PG_UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(15), nullable=False)
    created_at: Mapped = mapped_column(server_default="now()")

    # **** colunas “planas” para o composite ****
    rua:    Mapped[str] = mapped_column(String, nullable=False)
    bairro: Mapped[str] = mapped_column(String, nullable=False)
    cidade: Mapped[str] = mapped_column(String, nullable=False)
    estado: Mapped[str] = mapped_column(SQLEnum(Estado, name="estado_enum"), nullable=False)
    cep:    Mapped[str] = mapped_column(String(9), nullable=False)

    # **** aqui fazemos o “embutimento” ****
    endereco: Endereco = composite(Endereco, rua, bairro, cidade, estado, cep)

    # ex: relação muitos-para-muitos de roles…
    roles = relationship("Role", secondary=users_roles, lazy="joined")

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
