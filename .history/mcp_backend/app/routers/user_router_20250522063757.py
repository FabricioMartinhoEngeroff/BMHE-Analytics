from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from mcp_backend.app.config.database import get_db
from mcp_backend.app.domain.schemas.user import UserRequest, UserDTO
from mcp_backend.app.services.user_service import UserService
from mcp_backend.app.services.WhatsAppService import 
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.security.token_service import PasswordEncoder
from mcp_backend.app.services.WhatsAppService import WhatsAppService

router = APIRouter(prefix="/user", tags=["Usuários"])

user_repo = UserRepository()
whatsapp_service = WhatsAppService()
welcome_service = WelcomeService(whatsapp_service)
password_encoder = PasswordEncoder()
user_service = UserService(user_repo, password_encoder, welcome_service)

# GET /user/{user_id}
@router.get("/{user_id}", response_model=UserDTO)
def find_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    return user_service.find_user_by_id(db, user_id)

# POST /user/
@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def create_user(dto: UserRequest, db: Session = Depends(get_db)):
    return user_service.create_user(db, dto)

# PUT /user/{user_id}
@router.put("/{user_id}", response_model=UserDTO)
def update_user(user_id: UUID, dto: UserRequest, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, dto)

# DELETE /user/{user_id}
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None
