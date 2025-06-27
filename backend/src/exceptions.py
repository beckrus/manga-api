from fastapi import HTTPException


class BaseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Something went wrong"

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = "Object not found"


class AuthorNotFoundException(BaseException):
    detail = "Author not found"


class AuthorNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Author not found"


class AuthorDuplicateException(BaseException):
    detail = "Author already exist"


class AuthorDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Author already exist"


class ObjectDuplicateException(BaseException):
    detail = "Object already exist"


class FKObjectNotFoundException(BaseException):
    detail = "Foreign Key Object not found"


class MangaDuplicateException(BaseException):
    detail = "Manga already exist"


class MangaNotFoundException(BaseException):
    detail = "Manga not found"


class MangaNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Manga not found"


class MangaDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Manga already exist"


class ChapterNotFoundException(BaseException):
    detail = "Chapter not found"


class ChapterDuplicateException(BaseException):
    detail = "Chapter already exist"


class ChapterNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Chapter not found"


class ChapterDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Chapter already exist"


class BadFileExtException(BaseException):
    detail = "File must be a .zip archive."


class BadFileExtHTTPException(BaseHTTPException):
    status_code = 400
    detail = "File must be a .zip archive."


class BadImageFileExtException(BaseException):
    detail = "File does not have one of the allowed extensions"


class BadImageFileExtHTTPException(BaseHTTPException):
    detail = "File does not have one of the allowed extensions. Allowed extensions: .jpg, .jpeg, .png, .webp"


class BadFileExtInArchiveException(BaseException):
    detail = "File inside the ZIP archive does not have one of the allowed extensions"


class BadFileExtInArchiveHTTPException(BaseHTTPException):
    detail = "File inside the ZIP archive does not have one of the allowed extensions. Allowed extensions: .jpg, .jpeg, .png, .webp"


class PageNotFoundException(BaseException):
    detail = "Page not found"


class PageNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Page not found"


class PageDuplicateException(BaseException):
    detail = "Page already exist"


class PageDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Page already exist"


class PageFileImageNameException(BaseException):
    detail = "Images in the file should be named in numeric"


class PageFileImageNameHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Images in the file should be named in numeric"


class UserNotFoundException(BaseException):
    detail = "User not found"


class UserNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "User not found"


class UserDuplicateException(BaseException):
    detail = "User already exist"


class UserDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "User already exist"


class PasswordMatchException(BaseException):
    detail = "Passwords don't match"


class PasswordMatchHTTPException(BaseHTTPException):
    status_code = 422
    detail = "Passwords don't match"


class UserAuthException(BaseException):
    detail = "Invalid username or password"


class UserAuthHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Invalid username or password"


class TokenErrorHttpException(BaseHTTPException):
    status_code = 401
    detail = "Invalid token"


class AccessForbiddenException(BaseHTTPException):
    status_code = 401
    detail = "Access denied"


class AccessForbiddenHttpException(BaseHTTPException):
    status_code = 401
    detail = "Access denied"


class AlreadyRegisteredHttpException(BaseHTTPException):
    status_code = 401
    detail = "You are logged in. Log out and register a new account."


class FavoriteNotFoundException(BaseException):
    detail = "This manga not in the favorite"


class FavoriteNotFoundHttpException(BaseHTTPException):
    status_code = 404
    detail = "This manga not in the favorite"


class FavoriteDuplicateException(BaseException):
    detail = "This manga already in the favorite"


class FavoriteDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "This manga already in the favorite"


class CommentDuplicateException(BaseException):
    detail = "You can leave only one comment"


class CommentDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "You can leave only one comment for manga"


class CommentNotFoundException(BaseException):
    detail = "Commetn not found"


class CommentNotFoundHttpException(BaseHTTPException):
    status_code = 404
    detail = "Commetn not found"


class RedisConnectionError(BaseException):
    detail = "Failed to established Redis connection"


class PurchasesChapterDuplicateException(BaseException):
    detail = "The chapter's already been purchased"


class PurchasesChapterDuplicateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "The chapter's already been purchased"


class ChapterIsFreeException(BaseException):
    detail = "Chapter is free"


class ChapterIsFreeHTTPException(BaseHTTPException):
    status_code = 400
    detail = "Chapter is free"


class ChapterIsNotPurchasedException(BaseException):
    detail = "Chapter is premium"


class ChapterIsNotPurchasedHTTPException(BaseHTTPException):
    status_code = 401
    detail = "The chapter is premium, you have to buy it to access it"


class NotEnoughtCoinsException(BaseException):
    detail = "Chapter is free"


class NotEnoughtCoinsHTTPException(BaseHTTPException):
    status_code = 400
    detail = "Need more gold"


class RefreshTokenExpiredException(BaseException):
    detail = "Refresh Token expired"


class RefreshTokenExpiredHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Refresh Token expired"


class RefreshTokenNotFoundException(BaseException):
    detail = "Refresh Token not found"


class RefreshTokenNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Refresh Token not found"


class GoogleAuthFailedUserInfoException(BaseException):
    detail = "Google authentication failed: unable to obtain user details"


class GoogleAuthFailedHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Google authentication failed"
