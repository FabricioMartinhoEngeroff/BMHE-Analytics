from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.exceptions.security_exceptions import UnauthorizedException

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, token_service: TokenService, user_repository: UserRepository):
        super().__init__(app)
        self.token_service = token_service
        self.user_repository = user_repository

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/auth") or request.url.path.startswith("/docs"):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            raise UnauthorizedException("Token não informado")

        payload = self.token_service.validate_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Token inválido")

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("Usuário não encontrado")

        request.state.user = user
        return await call_next(request)
