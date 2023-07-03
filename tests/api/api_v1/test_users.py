import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from tests.utils.utils import random_lower_string, random_email
from tests.utils.users import create_random_user, get_auth_token_header


@pytest.mark.asyncio
async def test_read_users(client: AsyncClient, db: AsyncSession) -> None:
    password = random_lower_string()
    user = await create_random_user(db, password=password)
    headers = await get_auth_token_header(
        client, email=user.email, password=password
    )
    r = await client.get(
        f"{settings.API_V1_STR}/users/",
        headers=headers,
    )
    user_list = r.json()
    assert 200 <= r.status_code < 300
    for user in user_list:
        assert await crud.user.get_by_email(db, email=user["email"])


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db: AsyncSession) -> None:
    data = {
        "email": random_email(),
        "name": random_lower_string(),
        "password": random_lower_string(),
    }
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )
    assert await crud.user.get_by_email(db, email=data["email"])
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_existing_user(client: AsyncClient, db: AsyncClient) -> None:
    email = random_email()
    name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=name, password=password)
    user = await crud.user.create(db, obj_in=user_in)
    user_id = user.id
    headers = await get_auth_token_header(
        client, email=email, password=password
    )
    r = await client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = await crud.user.get_by_email(db, email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]
