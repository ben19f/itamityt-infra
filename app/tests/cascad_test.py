import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# tests/cascad_test.py
# tests/cascad_test.py
# tests/cascad_test.py
import pytest
import uuid
from fastapi import FastAPI
from httpx import AsyncClient
from main import app  # твое FastAPI приложение

@pytest.mark.anyio
async def test_user_delete_with_items():
    uid = uuid.uuid4().hex
    username = f"user_{uid}"
    email = f"{uid}@example.com"
    password = "testpass"

    # используем контекстный менеджер AsyncClient с app=app из fastapi.testclient
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # 1️⃣ регистрация
        response = await client.post(
            "/users/register",
            json={"username": username, "email": email, "password": password}
        )
        assert response.status_code == 201
        user_id = response.json()["id"]

        # 2️⃣ логин
        response = await client.post(
            "/auth/login",
            json={"email": email, "password": password}
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3️⃣ создаём item
        response = await client.post(
            "/items/",
            headers=headers,
            json={"name": "Item 1", "description": "desc1"}
        )
        assert response.status_code == 201
