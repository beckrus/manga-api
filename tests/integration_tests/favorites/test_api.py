from httpx import AsyncClient


async def test_favorites_flow_auth(
    ac_auth: AsyncClient,
):
    res_get = await ac_auth.get(
        "/manga",
    )
    assert res_get.status_code == 200
    manga_list = res_get.json()

    res_get_fav = await ac_auth.get(
        "/favorites",
    )
    assert res_get_fav.status_code == 200
    fav_list = res_get_fav.json()
    assert len(fav_list) == 0

    res_post = await ac_auth.post(
        "/favorites",
        data={"manga_id": manga_list[0]["id"]},
    )

    assert res_post.status_code == 204

    res_get_fav_2 = await ac_auth.get("/favorites")
    assert res_get_fav_2.status_code == 200
    fav_list = res_get_fav_2.json()
    assert len(fav_list) == 1
    assert fav_list[0]["id"] == manga_list[0]["id"]

    res_del = await ac_auth.request(
        "DELETE",
        "/favorites",
        data={"manga_id": manga_list[0]["id"]},
    )
    assert res_del.status_code == 204
    res_get_fav_3 = await ac_auth.get("/favorites")
    assert res_get_fav_3.status_code == 200
    fav_list = res_get_fav_3.json()
    assert len(fav_list) == 0


async def test_favorites_flow_wo_auth(
    ac: AsyncClient,
):
    res_get = await ac.get(
        "/manga",
    )
    assert res_get.status_code == 200
    manga_list = res_get.json()

    res_get_fav = await ac.get(
        "/favorites",
    )
    assert res_get_fav.status_code == 401

    res_post = await ac.post(
        "/favorites",
        data={"manga_id": manga_list[0]["id"]},
    )

    assert res_post.status_code == 401
