from datetime import datetime
from sqlalchemy import delete, insert, select

from src.exceptions import RefreshTokenExpiredException
from src.services.token import TokenService
from src.repositories.mappers.mappers import RefreshTokensMapper
from src.models.refresh_tokens import RefreshTokensOrm
from src.repositories.base import BaseRepository
from src.schemas.refresh_tokens import RefreshTokenAddDTO, RefreshTokenResponseDTO


class RefreshTokensRepository(BaseRepository):
    model = RefreshTokensOrm
    mapper = RefreshTokensMapper

    async def get_token(self, token: str) -> RefreshTokenResponseDTO:
        token_hash = TokenService.hash_token(token)
        query = select(self.model).filter_by(token_hash=token_hash)
        result = await self.session.execute(query)
        token = result.scalars().one_or_none()
        if token and token.expires_at > datetime.now():
            return token
        raise RefreshTokenExpiredException

    async def add_token(self, user_id: int) -> str:
        token = TokenService.create_refresh_token()
        token_hash = TokenService.hash_token(token)
        data = RefreshTokenAddDTO.model_validate({"user_id": user_id, "token_hash": token_hash})
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        await self.session.execute(stmt)
        return token

    async def delete_users_tokens(self, user_id: int) -> None:
        stmt = delete(self.model).filter_by(user_id=user_id)
        await self.session.execute(stmt)
        await self.session.commit()
