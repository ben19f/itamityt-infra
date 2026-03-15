import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.deps import get_db

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_URL_TEST, future=True, echo=False)
AsyncSessionLocal = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def async_client():
    # оборачиваем app через asgi_lifespan, чтобы работал context manager
    from asgi_lifespan import LifespanManager
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client

@pytest.mark.anyio
async def test_user_register(async_client):
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = await async_client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
