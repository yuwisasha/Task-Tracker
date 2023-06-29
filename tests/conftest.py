import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.db.session import AsyncSessionLocal
from app.core.config import settings
from tests.crud import TestUser


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()
        await session.rollback()


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as c:
        yield c


# Get a token for test endpoints which need auth user
@pytest_asyncio.fixture(scope="module")
async def token_header(client: AsyncClient) -> dict[str, str]:
    login_data = {
        "username": TestUser.NEW_EMAIL,
        "password": TestUser.PASSWORD,
    }
    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    token = response.json()
    print(token)
    access_token = token["access-token"]
    header = {"Authorization": f"Bearer {access_token}"}
    return header
