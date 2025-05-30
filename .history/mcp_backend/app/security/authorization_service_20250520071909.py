from mcp_backend.app.domain.modelsuser import User
from mcp_backend.app.exceptions.security_exceptions import ForbiddenException

class AuthorizationService:
    @staticmethod
    def authorize(user: User, required_role: str):
        if required_role not in user.roles:
            raise ForbiddenException("Você não tem permissão para acessar este recurso")
