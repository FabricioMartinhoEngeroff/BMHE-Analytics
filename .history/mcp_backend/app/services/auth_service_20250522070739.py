
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from mcp_backend.app.domain.schemas.auth import (
    LoginRequest, RegisterRequest, TokenResponse, UserProfileResponse
)
from mcp_backend.app.domain.models.user import User
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.repositories.role_repo import RoleRepository
from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.security.password_encoder import PasswordEncoder
from mcp_backend.app.exceptions.http_exceptions import (
    DuplicateResourceException, ResourceNotFoundException
)

class AuthService:
    def __init__(self):
        self.user_repo   = UserRepository()
        self.role_repo   = RoleRepository()
        self.token_svc   = TokenService()
        self.encoder     = PasswordEncoder()

    async def register(self, db: AsyncSession, data: RegisterRequest) -> TokenResponse:
        # 1) Verifica email duplicado
        if await self.user_repo.exists_by_email(db, data.email):
            raise DuplicateResourceException("Email já está em uso.")

        # 2) Pega a role padrão
        role = await self.role_repo.find_by_name(db, "ROLE_USER")
        if not role:
            raise ResourceNotFoundException("Permissão padrão não encontrada.")

        # 3) Cria o usuário
        hashed_password = self.encoder.encode(data.password)
        new_user = User(
            name=data.name,
            email=data.email,
            password=hashed_password,
            cpf=data.cpf,
            telefone=data.telefone,
            endereco=data.endereco,
            roles=[role]
        )

        # 4) Persiste no banco
        user = await self.user_repo.save(db, new_user)

        # 5) Gera token de acesso
        token = self.token_svc.generate_token(user.id)
        return TokenResponse(token=token)

    async def login(self, db: AsyncSession, data: LoginRequest) -> TokenResponse:
        # 1) Busca usuário
        user = await self.user_repo.find_by_email(db, data.email)
        # 2) Verifica senha
        if not user or not self.encoder.verify(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas."
            )

        # 3) Gera token
        token = self.token_svc.generate_token(user.id)
        return TokenResponse(token=token)

    def profile(self, user: User) -> UserProfileResponse:
        return UserProfileResponse(
            name=user.name,
            email=user.email,
            cpf=user.cpf,
            telefone=user.telefone,
            endereco=user.endereco
        )
