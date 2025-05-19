from datetime import datetime
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    message: str        # Mensagem geral
    ex_message: str     # Mensagem da exceção (detalhe técnico)
    path: str           # Rota que gerou o erro
    status: str         # Código HTTP
    timestamp: datetime # Momento do erro
