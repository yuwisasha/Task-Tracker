import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.db.session import AsyncSessionLocal


@pytest_asyncio.fixture(scope="session")
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
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as client:
        yield client
