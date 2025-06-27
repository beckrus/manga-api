from src.models.comments import CommentsOrm
from src.repositories.mappers.mappers import CommentsMapper
from src.repositories.base import BaseRepository


class CommentsRepository(BaseRepository):
    model = CommentsOrm
    mapper = CommentsMapper
