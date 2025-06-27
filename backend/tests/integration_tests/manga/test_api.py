import pytest
from httpx import AsyncClient
from src.schemas.manga import MangaDBAddDTO


@pytest.mark.parametrize(
    "data",
    [
        {
            "author": 18,
            "main_name": "One Piece",
            "secondary_name": "ワンピース",
            "description": "A story about pirates searching for the ultimate treasure.",
            "image": "one_piece.jpg",
            "created_by": 1,
        },
        {
            "author": 19,
            "main_name": "Naruto",
            "secondary_name": "ナルト",
            "description": "A ninja's journey to become the Hokage.",
            "image": "naruto.jpg",
            "created_by": 1,
        },
        {
            "author": 20,
            "main_name": "Bleach",
            "secondary_name": "ブリーチ",
            "description": "A story about a substitute soul reaper fighting hollows.",
            "image": "bleach.jpg",
            "created_by": 1,
        },
    ],
)
async def test_manga_flow_auth(
    data: dict,
    ac_auth: AsyncClient,
):
    manga_data = MangaDBAddDTO.model_validate(data)

    res_get = await ac_auth.get("/manga?page=1&per_page=100&sort=ASC")
    get_data = res_get.json()
    assert res_get.status_code == 200
    res_post = await ac_auth.post(
        "/manga",
        json={**manga_data.model_dump()},
    )
    assert res_post.status_code == 200
    post_data = res_post.json()
    assert post_data["main_name"] == manga_data.main_name

    manga_id = post_data["id"]
    manga_new_main_name = manga_data.main_name + " NEW"
    res_patch = await ac_auth.patch(
        f"/manga/{manga_id}",
        json={
            "main_name": manga_new_main_name,
        },
    )
    assert res_patch.status_code == 200
    data_patch = res_patch.json()
    assert data_patch["id"] == manga_id
    assert data_patch["main_name"] == manga_new_main_name
    res_get_by_id = await ac_auth.get(f"/manga/{manga_id}")
    assert res_get_by_id.status_code == 200
    data_get_by_id = res_get_by_id.json()
    assert data_get_by_id["main_name"] == data_patch["main_name"]
    res_delete = await ac_auth.delete(f"/manga/{manga_id}")
    assert res_delete.status_code == 204
    res_get_after_delete = await ac_auth.get("/manga?page=1&per_page=100&sort=ASC")
    assert res_get_after_delete.status_code == 200
    data_get_after_delete = res_get_after_delete.json()
    assert len(data_get_after_delete) == len(get_data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "author": 18,
            "main_name": "One Piece",
            "secondary_name": "ワンピース",
            "description": "A story about pirates searching for the ultimate treasure.",
            "image": "one_piece.jpg",
            "created_by": 1,
        },
        {
            "author": 19,
            "main_name": "Naruto",
            "secondary_name": "ナルト",
            "description": "A ninja's journey to become the Hokage.",
            "image": "naruto.jpg",
            "created_by": 1,
        },
        {
            "author": 20,
            "main_name": "Bleach",
            "secondary_name": "ブリーチ",
            "description": "A story about a substitute soul reaper fighting hollows.",
            "image": "bleach.jpg",
            "created_by": 1,
        },
    ],
)
async def test_manga_flow_wo_auth(
    data: dict,
    ac: AsyncClient,
):
    manga_data = MangaDBAddDTO.model_validate(data)

    res_get = await ac.get("/manga?page=1&per_page=100&sort=ASC")
    get_data = res_get.json()
    assert res_get.status_code == 200
    res_post = await ac.post(
        "/manga",
        json={**manga_data.model_dump()},
    )
    assert res_post.status_code == 401
    res_patch = await ac.patch(
        f"/manga/{get_data[0]['id']}",
        json={
            "main_name": "blabla",
        },
    )
    assert res_patch.status_code == 401

    res_delete = await ac.delete(f"/manga/{get_data[0]['id']}")
    assert res_delete.status_code == 401
