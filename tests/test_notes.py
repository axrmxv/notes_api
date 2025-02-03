import pytest


# Тест для создания заметки
@pytest.mark.asyncio
async def test_create_note(client):
    # Регистрация пользователя
    response = await client.post(
        "/register",
        json={"username": "testuser", "password": "testpass", "role": "user"}
    )
    assert response.status_code == 200

    # Получение токена
    response = await client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Создание заметки
    note_data = {"title": "Test Note", "body": "This is a test note."}
    response = await client.post(
        "/api/v1/notes/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=note_data
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"
    assert response.json()["body"] == "This is a test note."
