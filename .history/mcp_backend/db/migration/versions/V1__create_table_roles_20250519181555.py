from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

import uuid

# Revisões do Alembic
revision = 'V1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabela roles
    op.create_table(
        'roles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True)
    )

    # Inserir valores iniciais
    op.execute(
        "INSERT INTO roles (id, name) VALUES "
        "('123e4567-e89b-12d3-a456-426614174000', 'ROLE_USER'),"
        "('123e4567-e89b-12d3-a456-426614174001', 'ROLE_ADMIN')"
    )


def downgrade():
    op.drop_table('roles')
