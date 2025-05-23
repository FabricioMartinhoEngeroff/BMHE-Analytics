from typing import List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
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
            pattern=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).+$",
            description="Senha forte com letra maiúscula, minúscula, número e caractere especial"
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
    endereco: Endereco = Field(..., description="Endereço completo")


# DTO de leitura completo
class UserDTO(BaseModel):
    id: UUID
    name: str
    roles: List[str]
    cpf: str
    telefone: str
    endereco: Endereco


# DTO de perfil resumido
class UserProfile(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    telefone: str
    endereco: Endereco
