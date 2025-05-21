from mcp_backend.app.domain.models.user import User
from mcp_backend.app.exceptions.security_exceptions import ForbiddenException

# Para services
class AuthorizationService:
    @staticmethod
    def authorize(user: User, required_role: str):
        role_names = [role.name for role in user.roles]
        if required_role not in role_names:
            raise ForbiddenException("Você não tem permissão para acessar este recurso")

# Para endpoints
def has_role(required_role: str):
    def checker(user: User = Depends(get_current_user)):
        role_names = [role.name for role in user.roles]
        if required_role not in role_names:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return user
    return Depends(checker)
