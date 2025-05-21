from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mcp_backend.app.config.settings import get_settings
from mcp_backend.app.exceptions.handlers import register_exception_handlers
from mcp_backend.app.security.auth_middleware import AuthMiddleware
from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.routers import auth_router, user_router

# Carrega as configurações (.env via pydantic)
settings = get_settings()

# Cria a aplicação FastAPI
app = FastAPI(title=settings.APP_NAME)

# 🔧 Configuração de CORS
def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ❗ Em produção, substitua por ["https://seusite.com"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

setup_cors(app)

# ⚠️ Tratamento global de exceções
register_exception_handlers(app)

# 🔐 Middleware de autenticação
token_service = TokenService()
user_repository = UserRepository()
app.add_middleware(
    AuthMiddleware,
    token_service=token_service,
    user_repository=user_repository
)

# 📣 Rotas da API
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

# ✅ Rota de verificação
@app.get("/")
def raiz():
    return {"mensagem": f"{settings.APP_NAME} rodando com FastAPI 🧐🚀"}
