"""empty message

Revision ID: dfdcaa715749
Revises: ff5a0f7e9c2d
Create Date: 2020-09-15 18:37:05.729531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfdcaa715749'
down_revision = 'ff5a0f7e9c2d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('kuvert', sa.Column('title', sa.Unicode))

def downgrade():
    op.drop_column('kuvert', 'title')
