"""add price

Revision ID: f2e362a5117c
Revises: 822e1cd1babe
Create Date: 2025-04-28 13:08:06.552316

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f2e362a5117c"
down_revision: Union[str, None] = "822e1cd1babe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("purchases_chapters", sa.Column("price", sa.Integer(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("purchases_chapters", "price")
