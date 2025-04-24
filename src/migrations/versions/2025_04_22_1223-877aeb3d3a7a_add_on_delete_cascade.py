"""add on_delete cascade

Revision ID: 877aeb3d3a7a
Revises: ae753e49bffb
Create Date: 2025-04-22 12:23:18.877956

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "877aeb3d3a7a"
down_revision: Union[str, None] = "ae753e49bffb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("chapters_manga_id_fkey", "chapters", type_="foreignkey")
    op.create_foreign_key(None, "chapters", "manga", ["manga_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "chapters", type_="foreignkey")
    op.create_foreign_key("chapters_manga_id_fkey", "chapters", "manga", ["manga_id"], ["id"])
