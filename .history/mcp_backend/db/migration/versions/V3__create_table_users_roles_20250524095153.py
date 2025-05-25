"""create table users_roles

Revision ID: V3
Revises: V2
Create Date: 2025-05-24 00:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revisões
revision = 'V3'
down_revision = 'V2'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users_roles',
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('role_id', UUID(as_uuid=True), sa.ForeignKey('roles.id'), primary_key=True),
    )

def downgrade():
    op.drop_table('users_roles')
