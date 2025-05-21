from fastapi import APIRouter, Depends, HTTPException, status, Request
from mcp_backend.app.domain.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserProfileResponse,
)
from mcp_backend.app.secur.token_service import TokenService
from mcp_backend.app.security.token_service import get_current_user
from mcp_backend.app.domain.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register_user(data: RegisterRequest):
    return await auth_service.register(data)

@router.post("/login", response_model=TokenResponse)
async def login_user(data: LoginRequest):
    return await auth_service.login(data)

@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return auth_service.profile(current_user)
