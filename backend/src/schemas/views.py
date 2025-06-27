from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress


class ViewsDTO(BaseModel):
    user_id: int
    manga_id: int


class TrackingInfo(BaseModel):
    user_id: int | None
    ip: IPvAnyAddress
