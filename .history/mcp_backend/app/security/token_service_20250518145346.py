import os
from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status

class TokenService:
    def __init__(self):
        self.secret = os.getenv("TOKEN_SECRET", "segredo-super-secreto")
        self.expiration_hours = int(os.getenv("TOKEN_EXPIRATION_HOURS", "6"))
        self.algorithm = "HS256"

    def generate_token(self, user_id: UUID) -> str:
        expire = datetime.utcnow() + timedelta(hours=self.expiration_hours)
        to_encode = {"sub": str(user_id), "exp": expire}
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def validate_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload.get("sub")
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

    def get_user_id_from_token(self, token: str) -> UUID:
        user_id_str = self.validate_token(token)
        try:
            return UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID inválido no token"
            )
