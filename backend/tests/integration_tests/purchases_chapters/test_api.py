from httpx import AsyncClient


async def test_purchases_chapters_flow_auth(ac_auth: AsyncClient):
    res_get_me = await ac_auth.get(
        "/auth/me",
    )
    user = res_get_me.json()
    assert res_get_me.status_code == 200

    res_get_chapters = await ac_auth.get(
        "/manga/1/chapters",
    )
    assert res_get_chapters.status_code == 200
    chapters = res_get_chapters.json()
    assert len(chapters) > 0
    for ch in chapters[:2]:
        res_get = await ac_auth.get(
            "/purchases/me",
        )
        assert res_get.status_code == 200
        get_len_purchases = len(res_get.json())
        assert get_len_purchases == 0

        res_post = await ac_auth.post("/purchases", data={"chapter_id": ch["id"]})

        assert res_post.status_code == 204 if ch["is_premium"] else 400

        if ch["is_premium"]:
            res_get_2 = await ac_auth.get("/purchases/me")

            assert res_get_2.status_code == 200
            get_len_purchases_2 = len(res_get_2.json())

            assert get_len_purchases_2 > get_len_purchases

            res_get_me_2 = await ac_auth.get(
                "/auth/me",
            )
            user_2 = res_get_me_2.json()
            assert user_2["coin_balance"] == user["coin_balance"] - ch["price"]


async def test_purchases_chapters_flow_wo_auth(
    ac: AsyncClient,
):
    res_get = await ac.get(
        "/purchases",
    )
    assert res_get.status_code == 401
    res_post = await ac.post(
        "/purchases",
        json={"chapter_id": 1},
    )
    assert res_post.status_code == 401
