import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "data",
    [
        {"number": 1, "price": 0, "is_premium": False},
        {"number": 2, "price": 10, "is_premium": True},
    ],
)
async def test_chapters_flow_auth(
    data: dict,
    ac_auth: AsyncClient,
):
    res_get = await ac_auth.get("/manga?page=1&per_page=100&sort=ASC")
    get_data = res_get.json()
    assert res_get.status_code == 200
    manga_id = get_data[0]["id"]
    with open("tests/data/sample_chapter_pages.zip", "rb") as f:
        res_post = await ac_auth.post(
            f"/manga/{manga_id}/chapters",
            files={"file": ("sample_chapter_pages.zip", f, "application/zip")},
            data=data,
        )
        assert res_post.status_code == 200
        post_data = res_post.json()
        assert post_data["number"] == data["number"]
        assert post_data["is_premium"] == data["is_premium"]

    res_get_ch = await ac_auth.get(f"/manga/{manga_id}/chapters/{post_data['id']}")
    assert res_get_ch.status_code == 200
    data_get_ch = res_get_ch.json()
    assert data_get_ch["id"] == manga_id
    assert data_get_ch["number"] == data["number"]
    res_get_pages = await ac_auth.get(f"/manga/{manga_id}/chapters/{post_data['id']}/pages")
    data_get_pages = res_get_pages.json()
    assert res_get_ch.status_code == 200
    assert len(data_get_pages) > 0

    res_delete = await ac_auth.delete(f"/manga/{manga_id}/chapters/{post_data['id']}")
    assert res_delete.status_code == 204

    res_get_after_delete = await ac_auth.get(f"/manga/{manga_id}/chapters/{post_data['id']}/pages")
    assert res_get_after_delete.status_code == 200
    data_get_after_delete = res_get_after_delete.json()
    assert len(data_get_after_delete) == 0
