from typing import Annotated

from fastapi import Depends

from schemas.filters import PaginationParamsSchema


PaginationDep = Annotated[PaginationParamsSchema, Depends()]
