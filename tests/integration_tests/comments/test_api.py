import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("manga_id, text, status_code", [(1, "Like", 200), (1, "Duplicate", 200)])
async def test_chapters_flow_auth(
    manga_id: int,
    text: str,
    status_code: int,
    ac_auth: AsyncClient,
):
    res_get = await ac_auth.get(
        f"/manga/{manga_id}/comments",
    )
    assert res_get.status_code == 200
    get_len_comments = len(res_get.json())
    res_post = await ac_auth.post(
        f"/manga/{manga_id}/comments",
        json={"text": text},
    )
    assert res_post.status_code == status_code
    if status_code != 200:
        return
    post_data = res_post.json()
    assert post_data["text"] == text

    res_get_2 = await ac_auth.get(f"/manga/{manga_id}/comments")
    assert res_get_2.status_code == 200
    get_len_comments_2 = len(res_get_2.json())
    assert get_len_comments_2 > get_len_comments

    new_text = "blabla"
    res_patch = await ac_auth.patch(
        f"/manga/{manga_id}/comments/{post_data['id']}",
        json={"text": new_text},
    )
    assert res_patch.status_code == 200
    data_patch = res_patch.json()
    assert data_patch["text"] == new_text

    res_delete = await ac_auth.delete(f"/manga/{manga_id}/comments/{data_patch['id']}")
    assert res_delete.status_code == 204

    res_get_after_delete = await ac_auth.get(f"/manga/{manga_id}/comments")
    assert res_get_after_delete.status_code == 200
    data_get_after_delete = res_get_after_delete.json()
    assert len(data_get_after_delete) == get_len_comments


@pytest.mark.parametrize("manga_id, text, status_code", [(1, "Like", 401)])
async def test_chapters_flow_wo_auth(
    manga_id: int,
    text: str,
    status_code: int,
    ac: AsyncClient,
):
    res_get = await ac.get(
        f"/manga/{manga_id}/comments",
    )
    assert res_get.status_code == 200
    res_post = await ac.post(
        f"/manga/{manga_id}/comments",
        json={"text": text},
    )
    assert res_post.status_code == status_code
