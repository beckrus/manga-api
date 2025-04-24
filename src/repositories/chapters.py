from src.models.chapters import ChaptersOrm
from src.repositories.mappers.mappers import ChaptersMapper
from src.repositories.base import BaseRepository


class ChaptersRepository(BaseRepository):
    model = ChaptersOrm
    mapper = ChaptersMapper
