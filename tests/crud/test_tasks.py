from dataclasses import dataclass

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.user import UserCreate
from .test_users import TestUser


@dataclass
class TestTask:
    __test__ = False

    ID = 1
    TITLE = "title"
    DESCRIPTION = "description"
    DEADLINE = "2023-06-29 12:10:24"


@pytest.mark.asyncio
async def test_task_create(db: AsyncSession) -> None:
    user_in = UserCreate(
        email=TestUser.NEW_EMAIL,
        name=TestUser.NEW_NAME,
        password=TestUser.PASSWORD,
    )
    await crud.user.create(db, obj_in=user_in)
    users = await crud.user.get_multi(db)
    task_in = TaskCreate(
        title=TestTask.TITLE,
        description=TestTask.DESCRIPTION,
        deadline=TestTask.DEADLINE,
        performers=users,
    )
    task = await crud.task.create(db, obj_in=task_in)
    assert task.title == TestTask.TITLE
    assert task.description == TestTask.DESCRIPTION


@pytest.mark.asyncio
async def test_update_task(db: AsyncSession) -> None:
    new_title = "example"
    new_description = "example"
    new_deadline = "2024-08-15 22:00:00"
    task = await crud.task.get(db, id=TestTask.ID)
    task_in = TaskUpdate(
        title=new_title, description=new_description, deadline=new_deadline
    )
    await crud.task.update(db, db_obj=task, obj_in=task_in)
    updated_task = await crud.task.get(db, TestTask.ID)
    assert task.description == updated_task.description
    assert task.deadline == updated_task.deadline


@pytest.mark.asyncio
async def test_get_multi_task(db: AsyncSession) -> None:
    tasks = await crud.task.get_multi(db)
    assert tasks is not None
    assert isinstance(tasks, (list, Task))
    assert len(tasks) >= 1


@pytest.mark.asyncio
async def test_get_multi_by_performer(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(db, email=TestUser.NEW_EMAIL)
    tasks = await crud.task.get_multi_by_performer(db, performer_id=user.id)
    assert isinstance(tasks, (list, User))
    assert len(tasks) >= 1
    assert tasks is not None
