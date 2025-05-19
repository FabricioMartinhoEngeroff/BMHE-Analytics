from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# Revisões do Alembic
revision = 'V3'
down_revision = 'V2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users_roles',
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('role_id', UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE')
    )

    op.execute(
        """
        INSERT INTO users_roles (user_id, role_id)
        VALUES (
            'd193afd4-9222-4150-aadb-5167405a771c',
            '123e4567-e89b-12d3-a456-426614174000'
        );
        """
    )


def downgrade():
    op.drop_table('users_roles')
