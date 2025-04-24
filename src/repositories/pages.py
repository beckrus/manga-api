from src.models.pages import PagesOrm
from src.repositories.mappers.mappers import PagesMapper
from src.repositories.base import BaseRepository


class PagesRepository(BaseRepository):
    model = PagesOrm
    mapper = PagesMapper
