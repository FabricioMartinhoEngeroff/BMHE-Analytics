
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mcp_backend.app.config.database import get_db
from mcp_backend.app.domain.schemas.auth import (
    LoginRequest, RegisterRequest, TokenResponse, UserProfileResponse
)
from mcp_backend.app.services.auth_service import AuthService
from mcp_backend.app.security.user_loader import get_current_user  

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_svc = AuthService()

@router.post("/register", response_model=TokenResponse)
async def register(dto: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await auth_svc.register(db, dto)

@router.post("/login", response_model=TokenResponse)
async def login(dto: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await auth_svc.login(db, dto)

@router.get("/me", response_model=UserProfileResponse)
def profile(current_user=Depends(get_current_user)):
    return auth_svc.profile(current_user)
