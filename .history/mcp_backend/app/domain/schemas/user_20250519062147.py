from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, constr
from mcp_backend.app.domain.schemas.endereco import Endereco

# DTO de criação com validações
from typing import Annotated
from pydantic import BaseModel, Field, constr
from mcp_backend.app.domain.schemas.endereco import Endereco  # ajuste conforme sua estrutura

class UserRequest(BaseModel):
    name: Annotated[
        str,
        Field(..., min_length=1, description="Nome não pode estar vazio")
    ]

    email: Annotated[
        str,
        constr(regex=r"(^[\w\.-]+@[\w\.-]+\.\w{2,}$)"),
        Field(..., description="Email deve ser válido")
    ]

    password: Annotated[
        str,
        constr(min_length=8, regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).+$"),
        Field(..., description="Senha forte com letra maiúscula, minúscula, número e caracteres especiais")
    ]

    cpf: Annotated[
        str,
        constr(regex=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"),
        Field(..., description="CPF no formato xxx.xxx.xxx-xx")
    ]

    telefone: Annotated[
        str,
        constr(regex=r"^\(\d{2}\)\s?\d{4,5}-\d{4}$"),
        Field(..., description="Telefone no formato (xx) xxxxx-xxxx")
    ]

    endereco: Endereco  # já é um modelo Pydantic, não precisa de Annotated


# DTO de leitura completo
class User(BaseModel):
    id: UUID
    name: str
    roles: List[str]
    cpf: str
    telefone: str
    endereco: Endereco

# DTO de perfil resumido
class UserProfile(BaseModel):
    name: str
    email: str
    cpf: str
    telefone: str
    endereco: Endereco
