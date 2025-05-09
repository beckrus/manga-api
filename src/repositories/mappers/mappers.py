from src.models.refresh_tokens import RefreshTokensOrm
from src.schemas.refresh_tokens import RefreshTokenResponseDTO
from src.models.purchases_chapters import PurchasesChaptersOrm
from src.schemas.purchases_chapters import PurchasesChaptersResponseDTO
from src.models.read_progress import ReadProgressOrm
from src.schemas.read_progress import ReadProgressDTO
from src.models.comments import CommentsOrm
from src.schemas.comments import CommentsResponseFullDTO
from src.schemas.favorites import FavoriteResponseMangaDTO
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
from src.models.favorites import FavoriteMangaOrm


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


class FavoriteMangaMapper(BaseMapper):
    model = FavoriteMangaOrm
    schema = FavoriteResponseMangaDTO


class CommentsMapper(BaseMapper):
    model = CommentsOrm
    schema = CommentsResponseFullDTO


class ReadProgressMapper(BaseMapper):
    model = ReadProgressOrm
    schema = ReadProgressDTO


class PurchasesChaptersMapper(BaseMapper):
    model = PurchasesChaptersOrm
    schema = PurchasesChaptersResponseDTO


class RefreshTokensMapper(BaseMapper):
    model = RefreshTokensOrm
    schema = RefreshTokenResponseDTO
