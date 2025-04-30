from pydantic import BaseModel


class PurchasesChaptersDBAddDTO(BaseModel):
    chapter_id: int
    user_id: int
    price: int


class PurchasesChaptersResponseDTO(PurchasesChaptersDBAddDTO):
    id: int
