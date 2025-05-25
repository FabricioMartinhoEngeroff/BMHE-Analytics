from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revisões
revision = 'V1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
    )
    # seeds
    op.execute(
        "INSERT INTO roles (id, name) VALUES "
        "('123e4567-e89b-12d3-a456-426614174000','ROLE_USER'),"
        "('123e4567-e89b-12d3-a456-426614174001','ROLE_ADMIN')"
    )

def downgrade():
    op.drop_table('roles')
