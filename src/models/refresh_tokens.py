from datetime import datetime, timedelta
import uuid
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from src.config import settings
from src.database import Base


def expire_after_minutes(minutes: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES):
    return datetime.now() + timedelta(minutes=minutes)


class RefreshTokensOrm(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=expire_after_minutes)
