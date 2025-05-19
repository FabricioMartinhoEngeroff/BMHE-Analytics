from fastapi import FastAPI
#from app.config.settings import settings
from app.config.cors import configure_cors
from app.config.settings import get_settings
from app.exceptions.handlers import register_exception_handlers
from app.security.auth_middleware import AuthMiddleware
from app.security.token_service import TokenService
from app.repositories.user_repo import UserRepository
from app.routers import auth_router, user_router

settings = get_settings()
app = FastAPI(title=settings.APP_NAME)

# CORS e exceções
configure_cors(app)
register_exception_handlers(app)

# Middlewares
token_service = TokenService()
user_repository = UserRepository()
app.add_middleware(AuthMiddleware, token_service=token_service, user_repository=user_repository)

print(settings.DATABASE_URL)
print(settings.DATABASE_URL)

# Rotas
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

@app.get("/")
def raiz():
    return {"mensagem": "BMHE iniciado com FastAPI 🧐🚀"}
