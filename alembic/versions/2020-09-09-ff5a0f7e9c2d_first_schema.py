"""First schema

Revision ID: ff5a0f7e9c2d
Revises: 
Create Date: 2020-09-09 20:51:25.193252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ff5a0f7e9c2d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "kuvert",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("content", sa.Unicode, nullable=False),
        sa.Column("opening_date", sa.Date, nullable=False),
        sa.Column("tag", sa.Unicode, nullable=True),
        sa.Column("title", sa.Unicode, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("kuvert")
    pass
