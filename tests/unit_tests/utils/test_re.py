import pytest
from src.utils.re import get_missing_fk


@pytest.mark.parametrize(
    "text, result",
    [
        (
            """insert or update on table "manga" violates foreign key constraint "manga_author_fkey"
        DETAIL:  Key (author)=(2) is not present in table "authors".""",
            ("author", "2"),
        ),
        (
            """insert or update on table "manga" violates foreign key constraint "manga_author_fkey"
        DETAIL:  Key (manga)=(1) is not present in table "authors".""",
            ("manga", "1"),
        ),
        (
            """insert or update on table "manga" violates foreign key constraint "manga_author_fkey"
        DETAIL:  Key (chapter)=(10) is not present in table "authors".""",
            ("chapter", "10"),
        ),
    ],
)
def test_get_missing_fk(text: str, result: tuple[str, str]):
    assert result == get_missing_fk(text)
