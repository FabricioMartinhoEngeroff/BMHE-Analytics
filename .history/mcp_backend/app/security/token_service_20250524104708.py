from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status

from mcp_backend.app.config.settings import get_settings


class TokenService:
    """
    Serviço de criação e validação de JWTs.
    Busca as configurações em Settings (pydantic).
    """
    def __init__(self):
        settings = get_settings()
        self.secret = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def generate_token(self, user_id: UUID) -> str:
        """
        Gera um JWT com o campo `sub` igual ao ID do usuário e expiração.
        """
        expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def validate_token(self, token: str) -> UUID:
        """
        Decodifica e valida o token, retornando o UUID do usuário.
        Lança HTTPException em caso de expirado ou inválido.
        """
        try:
            data = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        sub = data.get("sub")
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token sem campo 'sub'"
            )

        try:
            return UUID(sub)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campo 'sub' não é um UUID válido"
            )
