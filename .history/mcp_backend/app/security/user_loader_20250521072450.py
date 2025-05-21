from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from mcp_backend.app.repositories.user_repo import UserRepository
from fastapi import Request, Depends, HTTPException, status
from mcp_backend.app.domain.models.user import User

class UserLoader:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        # Injeta o repositório, mantendo o código desacoplado e testável

    def load_user_by_email(self, db: Session, email: str):
        user = self.repository.find_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user


async def get_current_user(request: Request) -> User:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado"
        )
    return user