from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository

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
