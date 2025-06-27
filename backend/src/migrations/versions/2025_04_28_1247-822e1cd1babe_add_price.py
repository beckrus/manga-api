"""add price

Revision ID: 822e1cd1babe
Revises: 3e1d3025ace2
Create Date: 2025-04-28 12:47:24.131965

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "822e1cd1babe"
down_revision: Union[str, None] = "3e1d3025ace2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("chapters", sa.Column("price", sa.Integer(), nullable=True))
    op.execute("UPDATE chapters SET price = 0")
    op.alter_column("chapters", "price", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("chapters", "price")
