import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/register",
        json={"username": "testuser", "password": "testpass", "role": "user"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "user"


@pytest.mark.asyncio
async def test_login_user(client):
    await client.post(
        "/register",
        json={"username": "testuser", "password": "testpass", "role": "user"}
    )
    response = await client.post("/token", data={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
