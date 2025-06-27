"""add purchases_chapters

Revision ID: 3e1d3025ace2
Revises: 74cf759faece
Create Date: 2025-04-28 12:20:50.940756

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e1d3025ace2"
down_revision: Union[str, None] = "74cf759faece"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "purchases_chapters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("chapter_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "chapter_id", name="_user_purchases_chapters"),
    )
    op.add_column("users", sa.Column("coin_balance", sa.Integer(), nullable=True))
    op.execute("UPDATE users SET coin_balance = 0")
    op.alter_column("users", "coin_balance", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "coin_balance")
    op.drop_table("purchases_chapters")
