"""add password for user

Revision ID: f6cb662c2746
Revises: 58a3b916a67b
Create Date: 2025-04-22 12:04:11.518653

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f6cb662c2746"
down_revision: Union[str, None] = "58a3b916a67b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("password_hash", sa.String(), nullable=True))
    op.execute("UPDATE users SET password_hash = 'password'")
    op.alter_column("users", "password_hash", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "password_hash")
