import pytest


@pytest.mark.asyncio
async def test_signup_success(client):
    response = await client.post(
        "/auth/signup",
        json={"email": "user@example.com", "password": "securepass123"},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Account created successfully."
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_signup_duplicate_email(client):
    payload = {"email": "dup@example.com", "password": "securepass123"}
    await client.post("/auth/signup", json=payload)
    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_signup_password_too_short(client):
    response = await client.post(
        "/auth/signup",
        json={"email": "short@example.com", "password": "abc"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/signup", json={"email": "login@example.com", "password": "password123"})
    response = await client.post("/auth/login", json={"email": "login@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Logged in successfully."
    assert "access_token" in response.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/signup", json={"email": "wrong@example.com", "password": "password123"})
    response = await client.post("/auth/login", json={"email": "wrong@example.com", "password": "badpass"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_email(client):
    response = await client.post("/auth/login", json={"email": "ghost@example.com", "password": "password123"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_disabled_account(client, db_session):
    await client.post("/auth/signup", json={"email": "disabled@example.com", "password": "password123"})
    from sqlalchemy import select as sa_select
    from database.database_models import UserMaster as UM
    result = await db_session.execute(sa_select(UM).where(UM.email == "disabled@example.com"))
    user = result.scalar_one()
    user.is_account_disabled = True
    await db_session.commit()

    response = await client.post("/auth/login", json={"email": "disabled@example.com", "password": "password123"})
    assert response.status_code == 403
    assert "disabled" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_refresh_issues_new_access_token(client):
    await client.post("/auth/signup", json={"email": "refresh@example.com", "password": "password123"})
    response = await client.post("/auth/refresh")
    assert response.status_code == 200
    assert response.json()["message"] == "Token refreshed successfully."
    assert "access_token" in response.cookies


@pytest.mark.asyncio
async def test_refresh_without_cookie_fails(client):
    response = await client.post("/auth/refresh")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_clears_cookies_and_revokes_token(client):
    await client.post("/auth/signup", json={"email": "logout@example.com", "password": "password123"})
    response = await client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully."

    refresh_response = await client.post("/auth/refresh")
    assert refresh_response.status_code == 401
