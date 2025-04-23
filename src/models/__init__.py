from src.models.authors import AuthorsOrm
from src.models.chapters import ChaptersOrm
from src.models.comments import CommentsOrm
from src.models.favorites import FavoriteManga
from src.models.manga import MangaOrm
from src.models.pages import PagesOrm
from src.models.users import UserOrm

all = [
    MangaOrm,
    UserOrm,
    CommentsOrm,
    FavoriteManga,
    AuthorsOrm,
    ChaptersOrm,
    PagesOrm,
]
