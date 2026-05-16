import pytest


async def _signup_and_login(client, email="me@example.com", password="password123"):
    await client.post("/auth/signup", json={"email": email, "password": password})
    return await client.post("/auth/login", json={"email": email, "password": password})


@pytest.mark.asyncio
async def test_get_me_returns_user_info(client):
    await _signup_and_login(client, "getme@example.com")
    response = await client.get("/user/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "getme@example.com"
    assert data["is_admin_user"] is False


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    response = await client.get("/user/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_profile(client):
    await _signup_and_login(client, "update@example.com")
    response = await client.put(
        "/user/me",
        json={"first_name": "Ada", "last_name": "Lovelace", "phone_number": "1234567890"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Profile updated successfully."

    me = await client.get("/user/me")
    assert me.json()["profile"]["first_name"] == "Ada"
    assert me.json()["profile"]["last_name"] == "Lovelace"


@pytest.mark.asyncio
async def test_delete_account(client):
    await _signup_and_login(client, "delete@example.com")
    response = await client.delete("/user/me")
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted successfully."

    me = await client.get("/user/me")
    assert me.status_code == 401
