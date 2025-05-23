# mcp_backend/app/main.py

from fastapi import FastAPI
from mcp_backend.app.config.settings import get_settings
from mcp_backend.app.config.database import engine, AsyncSessionLocal
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.security.password_encoder import PasswordEncoder
from mcp_backend.app.services.whatsapp_service import WhatsAppService
from mcp_backend.app.services.user_service import UserService
# ... outros imports ...

settings = get_settings()
app = FastAPI(title=settings.APP_NAME)

# configurações de CORS, middlewares, exceções etc.

# === instanciando os serviços ===
user_repo = UserRepository()
pwd_encoder = PasswordEncoder()
whatsapp_service = WhatsAppService(
    account_sid=settings.TWILIO_ACCOUNT_SID,
    auth_token=settings.TWILIO_AUTH_TOKEN,
    from_whatsapp=settings.TWILIO_WHATSAPP_FROM,
)
user_service = UserService(user_repo, pwd_encoder, whatsapp_service)

# agora você pode usar `user_service` dentro dos routers,
# por exemplo passando-o como dependência em cada endpoint.
