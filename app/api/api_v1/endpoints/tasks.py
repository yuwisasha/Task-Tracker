from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Task])
async def task_list(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    tasks = await crud.task.get_multi(db, skip=skip, limit=limit)
    return tasks


@router.get("/{user_id}", response_model=list[schemas.Task])
async def task_list_by_user_id(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    tasks = await crud.task.get_multi_by_performer(performer_id=user_id)
    return tasks


@router.post("/", response_model=schemas.Task)
async def create_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    # current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = await crud.task.create(db, obj_in=task_in)
    return task


@router.put("/{task_id}", response_model=schemas.Task)
async def update_task_by_id(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: int,
    task_in: schemas.Task,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = await crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="The task doesn't exist.",
        )
    task = await crud.task.update(db, db_obj=task, obj_in=task_in)
    return task
