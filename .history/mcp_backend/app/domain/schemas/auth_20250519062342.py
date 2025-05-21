from pydantic import BaseModel, EmailStr, Field, constr
from typing import Annotated
from mcp_backend.app.domain.schemas.endereco import Endereco

# DTO de Login

# DTO de Token
class Token(BaseModel):
    token: str
