# app/domain/models/role.py

import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Role(Base):
    __tablename__ = "roles"  # Define o nome da tabela no banco

    # Coluna ID com UUID como chave primária
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )

    # Coluna name não pode ser nula e deve ser única
    name: Mapped[str] = mapped_column(
        String, 
        unique=True, 
        nullable=False
    )

    # Construtor para facilitar a criação de instâncias
    def __init__(self, name: str):
        self.name = name

    # Representação textual para debug
    def __repr__(self) -> str:
        return f"<Role(name={self.name})>"
