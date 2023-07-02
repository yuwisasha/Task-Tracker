from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.models.task import Task
from .utils import random_datetime


async def create_random_task(
    db: AsyncSession, title: str, description: str
) -> Task:
    task_in = schemas.TaskCreate(
        title=title,
        description=description,
        deadline=random_datetime(),
    )
    task = await crud.task.create(db, obj_in=task_in)
    return task
