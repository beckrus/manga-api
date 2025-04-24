import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "name",
    [
        ("Riyoko Ikeda"),
        ("Moto Hagio"),
        ("Rumiko Takahashi"),
    ],
)
async def test_authors_api_flow(
    name: str,
    ac: AsyncClient,
):
    """
    Test the full CRUD flow for the authors API.

    Steps:
    1. **GET /authors**: Retrieve the initial list of authors and verify the response.
    2. **POST /authors**: Add a new author with the provided name and verify the response.
    3. **PATCH /authors/{author_id}**: Update the author's name and verify the response.
    4. **GET /authors/{author_id}**: Retrieve the updated author by ID and verify the response matches the updated data.
    5. **DELETE /authors/{author_id}**: Delete the author by ID and verify the response.
    6. **GET /authors**: Retrieve the list of authors again and verify the author was successfully deleted.

    Parameters:
    - **name** (str): The name of the author to be added, updated, and deleted.

    Assertions:
    - Verify the status codes for each API call.
    - Ensure the data returned by the API matches the expected values at each step.
    - Confirm the author is successfully removed from the list after deletion.
    """
    res_get = await ac.get("/authors")
    get_data = res_get.json()
    assert res_get.status_code == 200
    res_post = await ac.post(
        "/authors",
        json={
            "name": name,
        },
    )
    assert res_get.status_code == 200
    post_data = res_post.json()
    assert post_data["name"] == name

    author_id = post_data["id"]
    author_new_name = name + " NEW"
    res_patch = await ac.patch(
        f"/authors/{author_id}",
        json={
            "name": author_new_name,
        },
    )
    assert res_patch.status_code == 200
    data_patch = res_patch.json()
    assert data_patch["id"] == author_id
    assert data_patch["name"] == author_new_name
    res_get_by_id = await ac.get(f"/authors/{author_id}")
    assert res_get_by_id.status_code == 200
    data_get_by_id = res_get_by_id.json()
    assert data_get_by_id == data_patch
    res_delete = await ac.delete(f"/authors/{author_id}")
    assert res_delete.status_code == 204
    res_get_after_delete = await ac.get("/authors")
    assert res_get_after_delete.status_code == 200
    data_get_after_delete = res_get_after_delete.json()
    assert len(data_get_after_delete) == len(get_data)
