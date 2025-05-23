# mcp_backend/app/domain/models/user.py

import uuid
from sqlalchemy import String, Enum as SQLAEnum, Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    composite,
    relationship,
)

from mcp_backend.app.domain.base import registry
from mcp_backend.app.domain.models.role import Role
from mcp_backend.app.domain.schemas.endereco import Endereco
from mcp_backend.app.domain.schemas.estado import Estado


# 1) Base e tabela de associação many-to-many
Base = registry.generate_base()

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id")),
)


# 2) Entidade User, com as colunas “planas” do Endereco + composite
class User(Base):
    __tablename__ = "users"

    # campos principais
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str] = mapped_column(String(15), nullable=False)

    # **** colunas “planas” para o composite do Endereco ****
    rua:     Mapped[str] = mapped_column(String(255), nullable=False)
    bairro:  Mapped[str] = mapped_column(String(255), nullable=False)
    cidade:  Mapped[str] = mapped_column(String(255), nullable=False)
    estado:  Mapped[Estado] = mapped_column(
        SQLAEnum(Estado, name="estado_enum"), nullable=False
    )
    cep:     Mapped[str] = mapped_column(String(9), nullable=False)

    # 3) composite — junta as colunas acima num value-object Endereco
    endereco: Endereco = composite(
        Endereco,
        rua,
        bairro,
        cidade,
        estado,
        cep,
    )

    # 4) relacionamento many-to-many com Role
    roles = relationship(Role, secondary=users_roles, lazy="joined")

    def __repr__(self) -> str:
        return f"<User name={self.name} email={self.email}>"
