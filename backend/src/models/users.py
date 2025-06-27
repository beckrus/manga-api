from datetime import datetime
import typing
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if typing.TYPE_CHECKING:
    from src.models.manga import MangaOrm


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    coin_balance: Mapped[int] = mapped_column(default=100)

    favorite_manga: Mapped[list["MangaOrm"]] = relationship(
        back_populates="favorited_by", secondary="favorite_manga"
    )
