from src.models.purchases_chapters import PurchasesChaptersOrm
from src.repositories.mappers.mappers import PurchasesChaptersMapper
from src.repositories.base import BaseRepository


class PurchasesChaptersRepository(BaseRepository):
    model = PurchasesChaptersOrm
    mapper = PurchasesChaptersMapper
