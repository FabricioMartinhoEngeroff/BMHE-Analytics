from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.repositories.user_repo import UserRepository


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, token_service: TokenService, user_repository: UserRepository):
        super().__init__(app)
        self.token_service = token_service
        self.user_repository = user_repository

   async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(auth)

        request.state.user = None
        if scheme and scheme.lower() == "bearer" and token:
            try:
                user_id = self.token_service.get_user_id_from_token(token)
                db = SessionLocal()                       # ① abre a sessão
                user = self.user_repository.find_by_id(db, user_id)  
                request.state.user = user
            finally:
                db.close()                                # ② fecha a sessão

        return await call_next(request)
