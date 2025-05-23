from pydantic import BaseModel, EmailStr, Field, constr
from typing import Annotated
from mcp_backend.app.domain.schemas.endereco import Endereco

# DTO de Login
class LoginRequest(BaseModel):
    email: Annotated[
        EmailStr,
        Field(..., description="Email válido")
    ]
    password: Annotated[
        str,
        constr(min_length=8),
        Field(..., description="Senha com no mínimo 8 caracteres")
    ]

# DTO de Registro
cclass RegisterRequest(BaseModel):
    name: Annotated[
        str,
        Field(..., min_length=1, description="Nome obrigatório")
    ]
    email: Annotated[
        EmailStr,
        Field(..., description="Email válido")
    ]
    password: Annotated[
        str,
        Field(..., min_length=8, description="Senha forte: mínimo 8 caracteres, com maiúscula, minúscula, número e símbolo")
    ]
    cpf: Annotated[
        str,
        Field(..., pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", description="CPF no formato xxx.xxx.xxx-xx")
    ]
    telefone: Annotated[
        str,
        Field(..., pattern=r"^\(\d{2}\)\s?\d{4,5}-\d{4}$", description="Telefone no formato (xx) xxxxx-xxxx")
    ]
    endereco: Endereco

    @field_validator("password")
    @classmethod
    def validar_senha_forte(cls, valor: str):
        if (
            not re.search(r"[A-Z]", valor) or
            not re.search(r"[a-z]", valor) or
            not re.search(r"\d", valor) or
            not re.search(r"[\W_]", valor)
        ):
            raise ValueError("A senha deve conter: letra maiúscula, minúscula, número e símbolo")
        return valor

# ✅ DTO de resposta do token
class TokenResponse(BaseModel):
    token: str

# ✅ DTO de resposta do perfil do usuário
class UserProfileResponse(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    telefone: str
    endereco: Endereco
