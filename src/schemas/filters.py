from enum import Enum
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class SortParams(str, Enum):
    asc = "ASC"
    desc = "DESC"


class PaginationParamsSchema(BaseModel):
    sort: Annotated[
        SortParams,
        Query(
            description="Sort items in ascending (ASC) or descending (DESC) order.",
            default=SortParams.asc,
            examples=["ASC", "DESC"],
        ),
    ]
    page: Annotated[
        int,
        Query(
            description="The page number to retrieve, starting from 1", default=1, ge=1
        ),
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
