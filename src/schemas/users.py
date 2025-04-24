from pydantic import BaseModel


class UserAddDTO(BaseModel):
    username: str
    email: str
    password: str
    password_confirm: str


class UserDBAddDTO(BaseModel):
    username: str
    email: str
    password_hash: str


class UserPatchDTO(BaseModel):
    username: str | None
    email: str | None
    password: str | None
    password_confirm: str | None


class UserResponseDTO(BaseModel):
    username: str
    email: str
