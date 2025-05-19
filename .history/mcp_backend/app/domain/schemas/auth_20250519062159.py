from pydantic import BaseModel, EmailStr, Field, constr
from typing import Annotated
from app.domain.schemas.endereco import Endereco

from typing import Annotated
from pydantic import BaseModel, Field, constr
from app.schemas.endereco import Endereco  # ajuste conforme sua estrutura

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


# DTO de Token
class Token(BaseModel):
    token: str
