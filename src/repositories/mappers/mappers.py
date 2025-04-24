from src.schemas.pages import PageResponseDTO
from src.models.pages import PagesOrm
from src.models.chapters import ChaptersOrm
from src.schemas.chapters import ChapterResponseDTO
from src.models.users import UserOrm
from src.schemas.users import UserResponseDTO
from src.schemas.manga import MangaResponseDTO
from src.models.manga import MangaOrm
from src.schemas.authors import AuthorResponseDTO
from src.models.authors import AuthorsOrm
from src.repositories.mappers.base import BaseMapper


class AuthorsMapper(BaseMapper):
    model = AuthorsOrm
    schema = AuthorResponseDTO


class MangaMapper(BaseMapper):
    model = MangaOrm
    schema = MangaResponseDTO


class UserMapper(BaseMapper):
    model = UserOrm
    schema = UserResponseDTO


class ChaptersMapper(BaseMapper):
    model = ChaptersOrm
    schema = ChapterResponseDTO


class PagesMapper(BaseMapper):
    model = PagesOrm
    schema = PageResponseDTO
