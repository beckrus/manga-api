from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class SortParams(str, Enum):
    asc = "ASC"
    desc = "DESC"


class PaginationParamsSchema(BaseModel):
    page: Annotated[
        int,
        Query(description="The page number to retrieve, starting from 1", default=1, ge=1),
    ]
    per_page: Annotated[
        int,
        Query(
            description="The number of items to display per page. Must be between 1 and 100.",
            default=10,
            ge=1,
            lt=101,
        ),
    ]
    sort: Annotated[
        SortParams,
        Query(
            description="Sort items in ascending (ASC) or descending (DESC) order.",
            default=SortParams.asc,
            examples=["ASC", "DESC"],
        ),
    ]


class MangaFilterSchema(BaseModel):
    name: Annotated[
        str | None,
        Query(
            default=None,
            description="Filter manga by name. Partial matches are allowed.",
        ),
    ]
    author: Annotated[
        str | None,
        Query(
            default=None,
            description="Filter manga by author name. Partial matches are allowed.",
        ),
    ]
