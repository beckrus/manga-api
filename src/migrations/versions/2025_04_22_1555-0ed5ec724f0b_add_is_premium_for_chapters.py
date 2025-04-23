"""add is_premium for chapters

Revision ID: 0ed5ec724f0b
Revises: 877aeb3d3a7a
Create Date: 2025-04-22 15:55:06.882763

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0ed5ec724f0b"
down_revision: Union[str, None] = "877aeb3d3a7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "chapters", sa.Column("is_premium", sa.Boolean(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("chapters", "is_premium")
