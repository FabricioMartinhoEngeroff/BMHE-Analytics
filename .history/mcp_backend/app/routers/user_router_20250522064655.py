from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from mcp_backend.app.config.database import get_db  # deve gerar AsyncSession
from mcp_backend.app.domain.schemas.user import UserRequest, UserDTO
from mcp_backend.app.services.user_service import UserService
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.security.password_encoder import PasswordEncoder
from mcp_backend.app.services.whatsapp_service import WhatsAppService

router = APIRouter(prefix="/user", tags=["Usuários"])

user_repo        = UserRepository()
password_encoder = PasswordEncoder()
whatsapp_service = WhatsAppService(
    account_sid="SID",
    auth_token="TOKEN",
    from_number="whatsapp:+14155238886"
)
user_service     = UserService(user_repo, password_encoder, whatsapp_service)

@router.get("/{user_id}", response_model=UserDTO)
async def find_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await user_service.find_user_by_id(db, user_id)

@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def create_user(dto: UserRequest, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, dto)

@router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: UUID, dto: UserRequest, db: AsyncSession = Depends(get_db)):
    return await user_service.update_user(db, user_id, dto)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    await user_service.delete_user(db, user_id)
    return None
