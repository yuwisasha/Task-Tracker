import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from tests.utils.users import create_random_user
from tests.utils.utils import random_lower_string, random_datetime


@pytest.mark.asyncio
async def test_create_task(db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    deadline = random_datetime()
    task_in = schemas.TaskCreate(
        title=title,
        description=description,
        deadline=deadline,
    )
    task = await crud.task.create(db, obj_in=task_in)
    assert task is not None
    assert task.title == title


@pytest.mark.asyncio
async def test_create_task_with_performers(db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    deadline = random_datetime()
    user_1 = await create_random_user(db)
    user_2 = await create_random_user(db)
    performers = [user_1, user_2]
    task_in = schemas.TaskCreate(
        title=title,
        description=description,
        deadline=deadline,
        performers=performers,
    )
    task = await crud.task.create(db, obj_in=task_in)
    # TODO
    ...
    