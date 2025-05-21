from fastapi import FastAPI
#from mcp_backend.app.config.settings import settings
from mcp_backend.app.config.cors import configure_cors
from mcp_backend.app.config.settings import get_settings
from mcp_backend.app.exceptions.handlers import register_exception_handlers
from mcp_backend.app.security.auth_middleware import AuthMiddleware
from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.routers import auth_router, user_router

app = FastAPI(title=settings.APP_NAME)

# CORS e exceções
configure_cors(app)
register_exception_handlers(app)

# Middlewares
token_service = TokenService()
user_repository = UserRepository()
app.add_middleware(AuthMiddleware, token_service=token_service, user_repository=user_repository)


settings = get_settings()
print(settings.DATABASE_URL)

# Rotas
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

@app.get("/")
def raiz():
    return {"mensagem": "BMHE iniciado com FastAPI 🧐🚀"}
