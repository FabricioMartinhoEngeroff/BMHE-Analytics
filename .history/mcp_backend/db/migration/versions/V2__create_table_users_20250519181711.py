from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

import uuid

# Revisões do Alembic
revision = 'V2'
down_revision = 'V1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('cpf', sa.String(14), nullable=False, unique=True),
        sa.Column('telefone', sa.String(15), nullable=False),
        sa.Column('rua', sa.String(255), nullable=False),
        sa.Column('bairro', sa.String(255), nullable=False),
        sa.Column('cidade', sa.String(255), nullable=False),
        sa.Column('estado', sa.String(30), nullable=False),
        sa.Column('cep', sa.String(9), nullable=False),
    )

    op.execute(
        """
        INSERT INTO users (
            id, name, email, password, cpf, telefone,
            rua, bairro, cidade, estado, cep
        ) VALUES (
            'd193afd4-9222-4150-aadb-5167405a771c',
            'Fabricio',
            'fa.engeroff1996@gmail.com',
            '$2a$10$3yHNGw3SkUYZECFGm3N9tOmXWQiS.K5/VYj3wVlTZzDrMGo5q6fRu',
            '031.044.320-23',
            '(51) 99640-7776',
            'Rua Das Bergamoteiras',
            'Nova Columbia',
            'Bom Princípio',
            'RS',
            '95765-000'
        );
        """
    )


def downgrade():
    op.drop_table('users')
