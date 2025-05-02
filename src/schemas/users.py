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
    is_admin: bool = False


class UserPatchDTO(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    password_confirm: str | None = None


class UserPatchCoinsDTO(BaseModel):
    coin_balance: int


class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    coin_balance: int


class UserFavManga(BaseModel):
    id: int
    main_name: str
    image: str


class UserResponseDTOwithRel(UserResponseDTO):
    favorite_manga: list[UserFavManga]


class UserLoginDTO(BaseModel):
    username: str
    password: str


class UserHashedPwdDTO(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str


class UserTokens(BaseModel):
    access_token: str
    refresh_token: str
