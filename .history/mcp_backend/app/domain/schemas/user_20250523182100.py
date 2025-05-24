from typing import List, Annotated
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from mcp_backend.app.domain.schemas.endereco import Endereco

# DTO de criação com validações
class UserRequest(BaseModel):
    name: Annotated[
        str,
        Field(..., min_length=1, description="Nome não pode estar vazio")
    ]
    email: Annotated[
        EmailStr,
        Field(..., description="Email deve ser válido")
    ]
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            description="Senha forte: mínimo 8 caracteres, com letra maiúscula, minúscula, número e símbolo"
        )
    ]
    cpf: Annotated[
        str,
        Field(..., pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", description="CPF no formato xxx.xxx.xxx-xx")
    ]
    telefone: Annotated[
        str,
        Field(..., pattern=r"^\(\d{2}\)\s?\d{4,5}-\d{4}$", description="Telefone no formato (xx) xxxxx-xxxx")
    ]
    endereco: Annotated[
        Endereco,
        Field(..., description="Endereço completo")
    ]

    @field_validator("password")
    @classmethod
    def validar_senha_forte(cls, pw: str) -> str:
        if not re.search(r"[A-Z]", pw):
            raise ValueError("A senha deve conter ao menos uma letra maiúscula")
        if not re.search(r"[a-z]", pw):
            raise ValueError("A senha deve conter ao menos uma letra minúscula")
        if not re.search(r"\d", pw):
            raise ValueError("A senha deve conter ao menos um número")
        if not re.search(r"[\W_]", pw):
            raise ValueError("A senha deve conter ao menos um caractere especial")
        return pw

# DTO de leitura completo
class UserDTO(BaseModel):
    id: UUID
    name: str
    roles: List[str]
    cpf: str
    telefone: str
    endereco: Endereco

# DTO de perfil resumido
class UserProfileResponse(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    telefone: str
    endereco: Endereco
