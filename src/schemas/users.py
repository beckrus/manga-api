from pydantic import BaseModel


class UserAddDTO(BaseModel):
    username: int
    email: str
    password: str | None
    password_confirm: str | None


class UserPatchDTO(BaseModel):
    username: int | None
    email: str | None
    password: str | None
    password_confirm: str | None
