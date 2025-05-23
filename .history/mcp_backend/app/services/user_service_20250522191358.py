# mcp_backend/app/services/user_service.py

import logging
from uuid import UUID
from sqlalchemy.orm import Session

from mcp_backend.app.domain.models.user import User, Role

from mcp_backend.app.domain.schemas.user import UserDTO, UserRequest
from mcp_backend.app.repositories.user_repo import UserRepository
from mcp_backend.app.security.password_encoder import PasswordEncoder
from mcp_backend.app.services.whatsapp_service import WhatsAppService
from mcp_backend.app.exceptions.http_exceptions import (
    MissingFieldException,
    DuplicateResourceException,
    ResourceNotFoundException,
)

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        password_encoder: PasswordEncoder,
        whatsapp_service: WhatsAppService,
    ):
        self.user_repo = user_repo
        self.password_encoder = password_encoder
        self.whatsapp_service = whatsapp_service

    def find_authenticated_user(self, db: Session, user_id: UUID) -> UserDTO:
        user = self.user_repo.find_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundException(f"Usuário não encontrado com ID: {user_id}")
        return UserDTO.from_orm(user)

    def find_user_by_id(self, db: Session, user_id: UUID) -> UserDTO:
        user = self.user_repo.find_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id: {user_id}")
        return UserDTO.from_orm(user)

    def create_user(self, db: Session, dto: UserRequest) -> UserDTO:
        self._validate_required_fields(dto)

        if self.user_repo.exists_by_email(db, dto.email):
            raise DuplicateResourceException("email", "A user with this email already exists.")
        if self.user_repo.exists_by_cpf(db, dto.cpf):
            raise DuplicateResourceException("cpf", "A user with this CPF already exists.")

        # 1) codifica a senha
        hashed = self.password_encoder.encode(dto.password)

        # 2) monta o composite de endereço
        endereco_model = EnderecoModel(
            rua=dto.endereco.rua,
            numero=dto.endereco.numero,
            cidade=dto.endereco.cidade,
            estado=dto.endereco.estado,
            cep=dto.endereco.cep
        )

        # 3) constrói a entidade User
        user = User(
            name=dto.name,
            email=dto.email,
            password=hashed,
            cpf=dto.cpf,
            telefone=dto.telefone,
            endereco=endereco_model,
        )

        # 4) atribui o papel padrão
        default_role = Role(name="ROLE_USER")
        user.roles.append(default_role)

        # 5) persiste
        saved = self.user_repo.save(db, user)

        # 6) envia mensagem de boas-vindas
        self.whatsapp_service.send_welcome_message(saved.telefone, saved.name)

        return UserDTO.from_orm(saved)

    def update_user(self, db: Session, user_id: UUID, dto: UserRequest) -> UserDTO:
        user = self.user_repo.find_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id: {user_id}")

        logger.debug("Before update: %s", user)
        self._update_user_fields(user, dto)
        updated = self.user_repo.save(db, user)
        logger.debug("After update: %s", updated)

        return UserDTO.from_orm(updated)

    def delete_user(self, db: Session, user_id: UUID) -> None:
        user = self.user_repo.find_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id: {user_id}")
        self.user_repo.delete(db, user)

    def _validate_required_fields(self, dto: UserRequest) -> None:
        for field in ("name", "email", "password", "cpf", "telefone"):
            value = getattr(dto, field)
            if not value or not value.strip():
                raise MissingFieldException(f"{field}", f"Field '{field}' cannot be empty")
        if not dto.endereco:
            raise MissingFieldException("endereco", "Address cannot be empty")

    def _update_user_fields(self, user: User, dto: UserRequest) -> None:
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

        # refatorado para usar o composite EnderecoModel
        if dto.endereco:
            user.endereco = EnderecoModel(
                rua=dto.endereco.rua,
                numero=dto.endereco.numero,
                cidade=dto.endereco.cidade,
                estado=dto.endereco.estado,
                cep=dto.endereco.cep
            )
