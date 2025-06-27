import hashlib
import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

from src.config import settings


class TokenService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def hash_token(cls, token: str) -> str:
        return hashlib.sha256((token + settings.JWT_SECRET_KEY).encode()).hexdigest()

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls) -> str:
        return secrets.token_urlsafe(64)

    @classmethod
    def decode_token(cls, token: str) -> dict[str, str | int]:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
