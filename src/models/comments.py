from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class CommentsOrm(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id", ondelete="CASCADE"))
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user = relationship("UserOrm", lazy="selectin")

    __table_args__ = (UniqueConstraint("user_id", "manga_id", name="_user_manga_comment"),)
