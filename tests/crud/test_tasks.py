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
    for performer in task.performers:
        assert performer
    assert len(task.performers) == 2


@pytest.mark.asyncio
async def test_update_task(db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    deadline = random_datetime()
    user = await create_random_user(db)
    task_in = schemas.TaskCreate(
        title=title,
        description=description,
        deadline=deadline,
        performers=[
            user,
        ],
    )
    task = await crud.task.create(db, obj_in=task_in)
    new_title = random_lower_string()
    new_user = await create_random_user(db)
    task_in_update = schemas.TaskUpdate(
        title=new_title,
        performers=[
            user,
            new_user,
        ],
    )
    await crud.task.update(db, db_obj=task, obj_in=task_in_update)
    task_2 = await crud.task.get(db, id=task.id)
    assert task.id == task_2.id
    assert len(task.performers) == len(task_2.performers)
    assert task.title == task_2.title
