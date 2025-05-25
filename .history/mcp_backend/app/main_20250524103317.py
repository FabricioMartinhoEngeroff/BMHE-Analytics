# mcp_backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from mcp_backend.app.config.settings import get_settings
from mcp_backend.app.config.database import get_db
from mcp_backend.app.exceptions.handlers import register_exception_handlers
from mcp_backend.app.security.auth_middleware import AuthMiddleware
from mcp_backend.app.security.token_service import TokenService
from mcp_backend.app.security.password_encoder import PasswordEncoder
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.services.whatsapp_service import WhatsAppService
from mcp_backend.app.services.user_service import UserService
from mcp_backend.app.routers import auth_router, user_router

settings = get_settings()
app = FastAPI(title=settings.APP_NAME)

# — CORS —
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Em produção, especifique sua(s) origem(ns)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# — Tratamento global de exceções —
register_exception_handlers(app)

# — Middleware de autenticação —
token_service = TokenService(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM
)
user_repository = UserRepository()
app.add_middleware(
    AuthMiddleware,
    token_service=token_service,
    user_repository=user_repository
)

# — Instanciação dos serviços de negócio —
pwd_encoder = PasswordEncoder()
whatsapp_service = WhatsAppService(
    account_sid=settings.TWILIO_ACCOUNT_SID,
    auth_token=settings.TWILIO_AUTH_TOKEN,
    from_number=settings.TWILIO_WHATSAPP_FROM
)
user_service = UserService(
    user_repo=user_repository,
    password_encoder=pwd_encoder,
    whatsapp_service=whatsapp_service
)

# — Provider do UserService para injeção de Depends —
def get_user_service() -> UserService:
    return user_service

# — Inclusão dos routers —  
#  - todos os endpoints terão acesso ao AsyncSession via Depends(get_db)
#  - e aos serviços via Depends(get_user_service) quando declarado no signature do endpoint
app.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(get_db)]
)
app.include_router(
    user_router.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_db), Depends(get_user_service)]
)

# — Health check / raiz —
@app.get("/", tags=["Root"])
async def health_check():
    return {"mensagem": f"{settings.APP_NAME} rodando com FastAPI 🧐🚀"}
