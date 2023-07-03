import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from tests.utils.utils import random_lower_string, random_datetime
from tests.utils.users import create_random_user, get_auth_token_header


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, db: AsyncSession) -> None:
    password = random_lower_string()
    user = await create_random_user(db, password=password)
    headers = await get_auth_token_header(
        client, user.email, password=password
    )
    title = random_lower_string()
    description = random_lower_string()
    deadline = random_datetime()
    data = {"title": title, "description": description, "deadline": deadline}
    r = await client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=headers,
        json=data,
    )
    task = r.json()
    assert r.status_code == 200
    assert task["title"] == title


@pytest.mark.asyncio
async def test_task_list(client: AsyncClient, db: AsyncSession) -> None:
    password = random_lower_string()
    user = await create_random_user(db, password=password)
    headers = await get_auth_token_header(
        client, user.email, password=password
    )
    for _ in range(2):
        title = random_lower_string()
        description = random_lower_string()
        deadline = random_datetime()
        data = {
            "title": title,
            "description": description,
            "deadline": deadline,
        }
        await client.post(
            f"{settings.API_V1_STR}/tasks/",
            headers=headers,
            json=data,
        )
    r = await client.get(
        f"{settings.API_V1_STR}/tasks/",
        headers=headers,
    )
    tasks = r.json()
    assert tasks
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_list_tasks_by_user_id(
    client: AsyncClient, db: AsyncSession
) -> None:
    password = random_lower_string()
    user = await create_random_user(db, password=password)
    headers = await get_auth_token_header(
        client, user.email, password=password
    )
    user_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    deadline = random_datetime()
    data = {
        "title": title,
        "description": description,
        "deadline": deadline,
        "performers": [
            {
                "email": user.email,
                "name": user.name,
                "id": user.id,
            }
        ],
    }
    await client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=headers,
        json=data,
    )
    r = await client.get(
        f"{settings.API_V1_STR}/tasks/{user_id}",
        headers=headers,
    )
    user_tasks = r.json()
    assert r.status_code == 200
    assert len(user_tasks) == 1
