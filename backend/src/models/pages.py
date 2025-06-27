from datetime import datetime
import typing
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.chapters import ChaptersOrm


class PagesOrm(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int]

    url: Mapped[str]

    chapter_id: Mapped[int] = mapped_column(
        ForeignKey("chapters.id", ondelete="CASCADE"), index=True
    )

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    chapter: Mapped["ChaptersOrm"] = relationship(back_populates="pages")

    __table_args__ = (UniqueConstraint("chapter_id", "number", name="_uniq_chapter_page"),)
