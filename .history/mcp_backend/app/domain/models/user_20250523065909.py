import uuid
from datetime import datetime

from sqlalchemy import String, func, Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite

from mcp_backend.app.config.database import Base
from mcp_backend.app.domain.models.role import Role
from mcp_backend.app.domain.models.endereco import Endereco  

Base = registry.generate_base()  # ou `declarative_base()` se não estiver usando registry

# Tabela intermediária users_roles (muitos para muitos)
users_roles = Table(
    "users_roles",
    Base.metadata,
    mapped_column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    mapped_column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"))
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name:     Mapped[str]       = mapped_column(String, nullable=False, unique=True)
    email:    Mapped[str]       = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str]       = mapped_column(String(255), nullable=False)
    cpf:      Mapped[str]       = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str]       = mapped_column(String(15), nullable=False)
    created_at: Mapped[datetime]= mapped_column(func.now(), init=False)

    # ——— colunas do composite Endereco ———
    rua:     Mapped[str] = mapped_column(String, nullable=False)
    bairro:  Mapped[str] = mapped_column(String, nullable=False)
    cidade:  Mapped[str] = mapped_column(String, nullable=False)
    estado:  Mapped[str] = mapped_column(String(2), nullable=False)  # 2 letras do enum
    cep:     Mapped[str] = mapped_column(String(9), nullable=False)

    # atributo composite que reúne as 5 colunas acima
    endereco: Endereco = composite(Endereco, rua, bairro, cidade, estado, cep)

    # relação muitos-para-muitos inalterada
    roles: Mapped[list[Role]] = relationship("Role", secondary=users_roles, lazy="joined")

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"