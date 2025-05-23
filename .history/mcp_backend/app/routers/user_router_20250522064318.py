from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from mcp_backend.app.config.database import get_db
from mcp_backend.app.domain.schemas.user import UserRequest, UserDTO
from mcp_backend.app.services.user_service import UserService
from mcp_backend.app.services.WhatsAppService import WhatsAppService
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.security.password_encoder import PasswordEncoder

router = APIRouter(prefix="/user", tags=["Usuários"])

# ✅ Configure corretamente as dependências
user_repo = UserRepository()
password_encoder = PasswordEncoder()
whatsapp_service = WhatsAppService(
    account_sid="SEU_TWILIO_ACCOUNT_SID",
    auth_token="SEU_TWILIO_AUTH_TOKEN",
    from_number="whatsapp:+14155238886"  # Número padrão do Twilio para WhatsApp
)

user_service = UserService(user_repo, password_encoder, whatsapp_service)

# Endpoints
@router.get("/{user_id}", response_model=UserDTO)
async def find_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    return await user_service.find_user_by_id(db, user_id)

@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def create_user(dto: UserRequest, db: Session = Depends(get_db)):
    return await user_service.create_user(db, dto)

@router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: UUID, dto: UserRequest, db: Session = Depends(get_db)):
    return await user_service.update_user(db, user_id, dto)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    await user_service.delete_user(db, user_id)
    return None
