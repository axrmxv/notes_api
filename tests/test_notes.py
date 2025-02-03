import pytest
from httpx import AsyncClient

from app.db.models import User
from app.core.security import create_access_token
from datetime import timedelta


# Фикстура для создания тестового пользователя
@pytest.fixture
def test_user():
    return User(id=1, username="testuser", role="user")


@pytest.fixture
def admin_user():
    return User(id=2, username="adminuser", role="admin")


# Фикстура для создания токена авторизации
def get_auth_headers(user: User):
    token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=15)
    )
    return {"Authorization": f"Bearer {token}"}


# Тест создания заметки
@pytest.mark.asyncio
async def test_create_note(client: AsyncClient, test_user: User):
    await client.post(
        "/register",
        json={"username": "testuser", "password": "testpass", "role": "user"}
    )
    headers = get_auth_headers(test_user)
    note_data = {"title": "Test Note", "body": "This is a test note."}

    response = await client.post(
        "/api/v1/notes/", json=note_data, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"


# Тест получения списка заметок пользователя
@pytest.mark.asyncio
async def test_get_user_notes(client: AsyncClient, test_user: User):
    await client.post(
        "/register",
        json={"username": "testuser", "password": "testpass", "role": "user"}
    )
    headers = get_auth_headers(test_user)

    response = await client.get("/api/v1/notes/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Тест получения заметки по ID
@pytest.mark.asyncio
async def test_get_note_by_id(client: AsyncClient, test_user: User):
    await client.post(
        "/register",
        json={"username": "testuser", "password": "testpass", "role": "user"}
    )
    headers = get_auth_headers(test_user)

    create_response = await client.post(
        "/api/v1/notes/",
        json={"title": "Note 1", "body": "Content"},
        headers=headers
    )
    note_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/notes/{note_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == note_id


# Тест обновления заметки
@pytest.mark.asyncio
async def test_update_note(client: AsyncClient, test_user: User):
    await client.post(
        "/register",
        json={"username": "testuser", "password": "testpass", "role": "user"}
    )
    headers = get_auth_headers(test_user)

    create_response = await client.post(
        "/api/v1/notes/",
        json={"title": "Note to Update", "body": "Old Content"},
        headers=headers
    )
    note_id = create_response.json()["id"]

    update_data = {"title": "Updated Title", "body": "Updated Content"}
    response = await client.put(
        f"/api/v1/notes/{note_id}", json=update_data, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]


# Тест удаления заметки
@pytest.mark.asyncio
async def test_delete_note(client: AsyncClient, test_user: User):
    headers = get_auth_headers(test_user)

    create_response = await client.post(
        "/api/v1/notes/",
        json={"title": "Note to Delete", "body": "Content"},
        headers=headers
    )
    note_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/notes/{note_id}", headers=headers)
    assert response.status_code == 200
    assert "удалена" in response.json()["message"]
