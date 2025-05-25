from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mcp_backend.app.config.database import get_db
from mcp_backend.app.domain.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse, UserProfileResponse
)
from mcp_backend.app.services.auth_service import AuthService
from mcp_backend.app.security.user_loader import get_current_user

router = APIRouter()

# o FastAPI vai injetar a instância auth_svc que você configurou em main.py
@router.post("/register", response_model=TokenResponse)
async def register(
    dto: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    auth_svc: AuthService = Depends()
):
    return await auth_svc.register(db, dto)

@router.post("/login", response_model=TokenResponse)
async def login(
    dto: LoginRequest,
    db: AsyncSession = Depends(get_db),
    auth_svc: AuthService = Depends()
):
    return await auth_svc.login(db, dto)

@router.get("/me", response_model=UserProfileResponse)
def me(
    current_user = Depends(get_current_user),
    auth_svc: AuthService = Depends()
):
    return auth_svc.profile(current_user)
