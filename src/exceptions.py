from fastapi import HTTPException


class BaseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Something went wrong"

    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=self.status_code, detail=self.detail, *args, **kwargs
        )


class ObjectNotFoundException(BaseException):
    detail = "Object not found"


class ObjectDuplicateException(BaseException):
    detail = "Object not found"
