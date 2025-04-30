"""add read_progress

Revision ID: 74cf759faece
Revises: a8deee4d9176
Create Date: 2025-04-28 08:35:02.692856

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "74cf759faece"
down_revision: Union[str, None] = "a8deee4d9176"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "read_progress_manga",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("manga_id", sa.Integer(), nullable=False),
        sa.Column("chapter_id", sa.Integer(), nullable=False),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["manga_id"], ["manga.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "manga_id", name="_user_manga_read_progress"),
    )
    op.create_unique_constraint("_user_manga_comment", "comments", ["user_id", "manga_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("_user_manga_comment", "comments", type_="unique")
    op.drop_table("read_progress_manga")
