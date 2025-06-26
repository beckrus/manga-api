"""add is_copleted

Revision ID: 813f97481375
Revises: e806376113ad
Create Date: 2025-06-26 10:13:43.472732

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "813f97481375"
down_revision: Union[str, None] = "e806376113ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("manga", sa.Column("is_completed", sa.Boolean(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("manga", "is_completed")
