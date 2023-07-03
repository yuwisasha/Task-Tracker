from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Body
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
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400, detail="User with this id doesn`t exist."
        )
    tasks = await crud.task.get_multi_by_performer(db, performer_id=user_id)
    return tasks


@router.post("/", response_model=schemas.Task)
async def create_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    title: str = Body(...),
    description: str = Body(...),
    deadline: datetime = Body(None),
    performers: list[schemas.User] = Body(None, embed=True),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    if performers:
        for perfomer in performers:
            user = await crud.user.get(db, id=perfomer.id)
            if not user:
                raise HTTPException(
                    status_code=400, detail="One of performers doesn`t exist."
                )
    task_in = schemas.TaskCreate(
        title=title,
        description=description,
        deadline=deadline,
        performers=performers,
    )
    task = await crud.task.create(db=db, obj_in=task_in)
    return task


@router.put("/{task_id}", response_model=schemas.Task)
async def update_task_by_id(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: int,
    task_in: schemas.TaskUpdate,
    # current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = await crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="The task doesn't exist.",
        )
    for performer in task_in.performers:
        user = await crud.user.get(db, id=performer.id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="One of performers doesn't exist.",
            )
    task = await crud.task.update(db, db_obj=task, obj_in=task_in)
    return task
