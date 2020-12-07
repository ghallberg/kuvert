"""add created_at column to kuvert

Revision ID: 8decf7e9c79b
Revises: ea080c51f97f
Create Date: 2020-12-02 21:44:11.696522

"""
from alembic import op
from datetime import datetime
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8decf7e9c79b"
down_revision = "ea080c51f97f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "kuvert",
        sa.Column(
            "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_column("kuvert", "created_at")
