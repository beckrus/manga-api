from datetime import datetime
import uuid
from pydantic import BaseModel


class RefreshTokenAddDTO(BaseModel):
    user_id: int
    token_hash: str


class RefreshTokenResponseDTO(RefreshTokenAddDTO):
    id: uuid.UUID
    created_at: datetime
    expires_at: datetime
