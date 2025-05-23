from typing import Optional
from uuid import UUID
import logging
from sqlalchemy.orm import Session

from domain.models.user import User, Role
from mcp_backend.app.domain.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserProfileResponse

from mcp_backend.app.repositories.user_repo import UserRepository
from security.token_service import PasswordEncoder
from services.welcome_service import WelcomeService
from exceptions.http_exceptions import (
    ResourceNotFoundException,
    DuplicateResourceException,
    MissingFieldException
)

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, user_repo: UserRepository, password_encoder: PasswordEncoder, welcome_service: WelcomeService):
        self.user_repo = user_repo
        self.password_encoder = password_encoder
        self.welcome_service = welcome_service

   
    def _validate_required_fields(self, dto: UserRequest):
        required = {
            "name": dto.name,
            "email": dto.email,
            "password": dto.password,
            "cpf": dto.cpf,
            "telefone": dto.telefone
        }
        for field, value in required.items():
            if not value or not value.strip():
                raise MissingFieldException(f"Field '{field}' cannot be empty")
            if not dto.endereco:
                raise MissingFieldException("Endereco cannot be empty")
        
        def find_user_by_id(self, db: Session, user_id: UUID) -> UserDTO:
            user = self.user_repo.find_by_id(db, user_id)
            if not user:
                raise ResourceNotFoundException(f"Usuário não encontrado com ID: {user_id}")
            return UserDTO.from_orm(user)

    def create_user(self, db: Session, data: UserRequest) -> UserDTO:
        self._validate_required_fields(data)

        if self.user_repo.exist_by_email(db, data.email):
            raise DuplicateResourceException("email", "A user with this email already exists.")

        if self.user_repo.exist_by_cpf(db, data.cpf):
            raise DuplicateResourceException("cpf", "A user with this CPF already exists.")

        encoded_password = self.password_encoder.encode(data.password)

        user = User(
            name=data.name,
            email=data.email,
            password=encoded_password,
            cpf=data.cpf,
            telefone=data.telefone,
            endereco=data.endereco
        )

        default_role = Role(name="ROLE_USER")
        user.roles.append(default_role)

        user = self.user_repo.save(db, user)

        self.welcome_service.enviar_boas_vindas(user.name, user.telefone)

        return UserDTO.from_orm(user)

    def update_user(self, db: Session, user_id: UUID, dto: UserRequest) -> UserDTO:
        user = self.user_repo.find_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id: {user_id}")

        logger.debug(f"Before update: {user}")
        self._update_user_fields(user, dto)
        user = self.user_repo.save(db, user)
        logger.debug(f"After update: {user}")

        return UserDTO.from_orm(user)
    
    def delete_user(self, user_id: UUID, db: Session):
        user = self.user_repo.find_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id: {user_id}")
        self.user_repo.delete(db, user)

    def _update_user_fields(self, user: User, dto: UserRequest):
        if dto.name:
            user.name = dto.name
        if dto.email:
            user.email = dto.email
        if dto.password and dto.password.strip():
            user.password = self.password_encoder.encode(dto.password)
        if dto.cpf:
            user.cpf = dto.cpf
        if dto.telefone:
            user.telefone = dto.telefone
        if dto.endereco:
            user.endereco = dto.endereco
