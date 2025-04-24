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
    status_code = (400,)
    detail = "File must be a .zip archive."


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
