from src.models.purchases_chapters import PurchasesChaptersOrm
from src.models.authors import AuthorsOrm
from src.models.chapters import ChaptersOrm
from src.models.comments import CommentsOrm
from src.models.favorites import FavoriteMangaOrm
from src.models.manga import MangaOrm
from src.models.pages import PagesOrm
from src.models.users import UserOrm
from src.models.read_progress import ReadProgressOrm
from src.models.refresh_tokens import RefreshTokensOrm

all = [
    MangaOrm,
    UserOrm,
    CommentsOrm,
    FavoriteMangaOrm,
    AuthorsOrm,
    ChaptersOrm,
    PagesOrm,
    ReadProgressOrm,
    PurchasesChaptersOrm,
    RefreshTokensOrm,
]
