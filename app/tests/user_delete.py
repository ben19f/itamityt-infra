import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# tests/test_user_delete.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    await client.__aenter__()
    yield client
    await client.__aexit__(None, None, None)

@pytest.mark.anyio
async def test_delete_user_with_items(async_client):
    # Создаем пользователя
    response = await async_client.post(
        "/users/register",
        json={"username": "deleteuser", "email": "delete@example.com", "password": "testpass"}
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Создаем item для пользователя
    response = await async_client.post(
        "/items/create",
        json={"name": "Item1", "user_id": user_id}
    )
    assert response.status_code == 201

    # Удаляем пользователя
    response = await async_client.delete(f"/users/delete/{user_id}")
    assert response.status_code == 204

    # Проверяем, что повторный запрос на удаление вернёт 404
    response = await async_client.delete(f"/users/delete/{user_id}")
    assert response.status_code == 404

    # Проверяем, что items удалились (можно через GET /items или через БД напрямую)
    response = await async_client.get(f"/items/user/{user_id}")
    assert response.status_code == 404 or response.json() == []
