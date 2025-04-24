"""change user_id to created_by

Revision ID: a8deee4d9176
Revises: 0ed5ec724f0b
Create Date: 2025-04-23 14:29:14.950956

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a8deee4d9176"
down_revision: Union[str, None] = "0ed5ec724f0b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("manga", sa.Column("created_by", sa.Integer(), nullable=False))
    op.drop_constraint("manga_user_id_fkey", "manga", type_="foreignkey")
    op.create_foreign_key(None, "manga", "users", ["created_by"], ["id"])
    op.drop_column("manga", "user_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "manga",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "manga", type_="foreignkey")
    op.create_foreign_key("manga_user_id_fkey", "manga", "users", ["user_id"], ["id"])
    op.drop_column("manga", "created_by")
