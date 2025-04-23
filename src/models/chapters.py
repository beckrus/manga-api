from datetime import datetime
import typing
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.pages import PagesOrm


class ChaptersOrm(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int]
    manga_id: Mapped[int] = mapped_column(
        ForeignKey("manga.id", ondelete="CASCADE"), index=True
    )

    pages: Mapped[list["PagesOrm"]] = relationship(
        back_populates="pages", cascade="all, delete-orphan"
    )
    is_premium: Mapped[bool] = mapped_column(default=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("manga_id", "number", name="_uniq_manga_chapter"),
    )
