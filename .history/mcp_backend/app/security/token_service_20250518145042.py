from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config.settings import settings
from app.exceptions.security_exceptions import UnauthorizedException

class TokenService:
    def create_token(self, user_id: str) -> str:
        expiration = datetime.utcnow() + timedelta(hours=2)
        payload = {
            "sub": user_id,
            "exp": expiration
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def validate_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except JWTError:
            raise UnauthorizedException("Token inválido ou expirado")
