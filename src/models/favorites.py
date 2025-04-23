from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class FavoriteManga(Base):
    __tablename__ = "favorite_manga"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    manga_id: Mapped[int] = mapped_column(ForeignKey("manga.id", ondelete="CASCADE"))
    __table_args__ = (
        UniqueConstraint("user_id", "manga_id", name="_user_manga_favorite"),
    )
