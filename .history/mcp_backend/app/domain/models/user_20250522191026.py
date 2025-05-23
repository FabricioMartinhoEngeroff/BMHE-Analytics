# mcp_backend/app/domain/models/user.py

import uuid
from datetime import datetime
from typing import List
from sqlalchemy import String, ForeignKey, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mcp_backend.app.domain.models.role import Role
from mcp_backend.app.domainmodels.base import registry

Base = registry.generate_base()

# tabela associativa users_roles (muitos-para-muitos)
users_roles = Table(
    "users_roles",
    Base.metadata,
    # aqui usamos Column puro porque mapped_column gera MappedColumn, que não serve pra Table()
    mapped_column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    mapped_column("role_id", UUID(as_uuid=True), ForeignKey("roles.id")),
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                          primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str]      = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str]     = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str]  = mapped_column(String(255), nullable=False)
    cpf: Mapped[str]       = mapped_column(String(14), nullable=False, unique=True)
    telefone: Mapped[str]  = mapped_column(String(15), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # << aqui na anotação usamos List[Role] e importamos List do typing >>
    roles: Mapped[List[Role]] = relationship(
        "Role",
        secondary=users_roles,
        lazy="joined",
        # opcional: garanta que sempre comece como lista vazia
        default_factory=list
    )

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
