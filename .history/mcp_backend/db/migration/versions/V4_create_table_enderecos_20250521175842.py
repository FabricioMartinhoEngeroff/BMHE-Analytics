"""create table enderecos"""

from alembic import op
import sqlalchemy as sa

revision = 'V4'
down_revision = 'V3'  
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'enderecos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('rua', sa.String, nullable=False),
        sa.Column('numero', sa.String, nullable=False),
        sa.Column('cidade', sa.String, nullable=False),
        sa.Column('estado', sa.String, nullable=False), 
    )


def downgrade():
    op.drop_table('enderecos')
