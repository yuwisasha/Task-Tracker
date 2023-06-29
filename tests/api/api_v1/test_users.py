import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.core.config import settings
from tests.crud import TestTask, TestUser


@pytest.mark.asyncio
async def test_get_users(
    client: AsyncClient, db: AsyncSession, token_header: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users", headers=token_header
    )
    users = response.json()
    assert users
