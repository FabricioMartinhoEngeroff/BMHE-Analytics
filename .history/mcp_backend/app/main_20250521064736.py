# main.py

from fastapi import FastAPI
from mcp_backend.app.config.settings import get_settings
from mcp_backend.app.config.settings import get_settings
from mcp_backend.app.exceptions.handlers import register_exception_handlers
from mcp_backend.app.security.auth_middleware import AuthMiddleware
from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.routers import auth_router, user_router

# Carrega as configurações (pydantic + .env)
settings = get_settings()

# Cria a aplicação
app = FastAPI(title=settings.APP_NAME)

# 🔧 CORS e tratamento de exceções
configure_cors(app)
register_exception_handlers(app)

# 🔐 Middleware de autenticação
token_service    = TokenService()
user_repository  = UserRepository()
app.add_middleware(
    AuthMiddleware,
    token_service=token_service,
    user_repository=user_repository
)

# 📣 Rotas da API
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

# Rota de sanity check
@app.get("/")
def raiz():
    return {"mensagem": f"{settings.APP_NAME} rodando com FastAPI 🧐🚀"}
