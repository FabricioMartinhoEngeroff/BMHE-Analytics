from sqlalchemy import Column, ForeignKey, Table, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
import uuid
from datetime import datetime
from mcp_backend.app.domain.models.role import Role
from mcp_backend.app.domain.models.base import registry

Base = registry.generate_base()  # ou declarative_base()

# ✅ Tabela associativa (usando Column corretamente)
users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"))
)
