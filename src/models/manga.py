from datetime import datetime
import typing
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.chapters import ChaptersOrm
    from src.models.users import UserOrm


class MangaOrm(Base):
    __tablename__ = "manga"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[int | None] = mapped_column(ForeignKey("authors.id"), index=True)

    main_name: Mapped[str]
    secondary_name: Mapped[str | None]

    rate: Mapped[int] = mapped_column(default=0)
    count_views: Mapped[int] = mapped_column(default=0)
    count_bookmarks: Mapped[int] = mapped_column(default=0)

    description: Mapped[str]
    image: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    chapters: Mapped[list["ChaptersOrm"]] = relationship(
        back_populates="manga", cascade="all, delete-orphan"
    )

    favorited_by: Mapped[list["UserOrm"]] = relationship(
        back_populates="favorite_manga", secondary="favorite_manga"
    )

    __table_args__ = (UniqueConstraint("author", "main_name", name="_uniq_manga"),)
