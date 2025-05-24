# app/security/auth_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException, status

from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.repositories.user_repo   import UserRepository
from app.config.database import get_db 

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        token_service: TokenService,
        user_repository: UserRepository
    ):
        super().__init__(app)
        self.token_service = token_service
        self.user_repository = user_repository

    async def dispatch(self, request: Request, call_next):
        # Por padrão não há usuário autenticado
        request.state.user = None

        # Pega o header Authorization
        auth = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(auth)

        # Se for Bearer <token>, tenta validar e buscar o usuário
        if scheme and scheme.lower() == "bearer" and token:
            try:
                # 1️⃣ Extrai o user_id do token (pode lançar HTTPException 401)
                user_id = self.token_service.get_user_id_from_token(token)

                # 2️⃣ Abre a sessão assíncrona com o banco
                async with get_db() as session:
                    # 3️⃣ Busca o usuário no repositório
                    user = await self.user_repository.find_by_id(session, user_id)

                # 4️⃣ Se encontrou, atribui ao request.state
                request.state.user = user

            except HTTPException:
                # token expirado ou inválido
                raise
            except Exception:
                # qualquer outro erro (ex.: DB offline) deixa user como None
                request.state.user = None

        # Chama o próximo handler
        response = await call_next(request)
        return response
