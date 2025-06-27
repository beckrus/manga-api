from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class PurchasesChaptersOrm(Base):
    __tablename__ = "purchases_chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"))
    price: Mapped[int]

    __table_args__ = (UniqueConstraint("user_id", "chapter_id", name="_user_purchases_chapters"),)
