import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "username, email, password, password_confirm, status_code",
    [
        ("jojo", "jojo@example.com", "123", "123", 200),
        ("jojo", "jojo1@example.com", "123", "123", 409),
        ("jojo1", "jojo@example.com", "123", "123", 409),
        ("bond", "james.bond@example.com", "007", "008", 422),
        ("bond", "james.bond@example.com", "007", "007", 200),
    ],
)
async def test_auth_api_flow(
    username: str,
    email: str,
    password: str,
    password_confirm: str,
    status_code: int,
    ac: AsyncClient,
):
    res_register = await ac.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
        },
    )
    register_data = res_register.json()
    assert res_register.status_code == status_code
    if status_code != 200:
        return
    assert register_data["username"] == username

    res_login = await ac.post("/auth/login", data={"username": username, "password": password})
    login_data = res_login.json()
    assert res_login.status_code == 200
    access_token = login_data.get("access_token")
    assert access_token
    headers = {"Authorization": f"Bearer {access_token}"}
    refresh_token = ac.cookies.get("refresh_token")
    assert refresh_token

    res_refresh = await ac.post("/auth/refresh-token", headers=headers)
    assert res_refresh.status_code == 200
    assert refresh_token != ac.cookies.get("refresh_token")
    refresh_data = res_refresh.json()
    access_token = refresh_data.get("access_token")
    assert access_token
    headers = {"Authorization": f"Bearer {access_token}"}

    res_me = await ac.get("/auth/me", headers=headers)
    me_data = res_me.json()
    assert res_me.status_code == 200
    assert me_data["username"] == username
    assert me_data["email"] == email

    res_logout = await ac.post("/auth/logout", headers=headers)
    assert res_logout.status_code == 200
    assert not ac.cookies.get("refresh_token")
    res_me = await ac.get("/auth/me")
    assert res_me.status_code == 401
