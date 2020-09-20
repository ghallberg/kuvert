"""Rename owner to tag

Revision ID: ea080c51f97f
Revises: dfdcaa715749
Create Date: 2020-09-20 19:12:33.545051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea080c51f97f'
down_revision = 'dfdcaa715749'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('kuvert', 'owner', new_column_name='tag')


def downgrade():
    op.alter_column('kuvert', 'tag', new_column_name='owner')
