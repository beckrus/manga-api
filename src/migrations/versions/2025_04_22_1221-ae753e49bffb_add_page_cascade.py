"""add page cascade

Revision ID: ae753e49bffb
Revises: f6cb662c2746
Create Date: 2025-04-22 12:21:31.807284

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ae753e49bffb"
down_revision: Union[str, None] = "f6cb662c2746"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("pages_chapter_id_fkey", "pages", type_="foreignkey")
    op.create_foreign_key(
        None, "pages", "chapters", ["chapter_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "pages", type_="foreignkey")
    op.create_foreign_key(
        "pages_chapter_id_fkey", "pages", "chapters", ["chapter_id"], ["id"]
    )
