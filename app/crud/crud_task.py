from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def create(self, db: AsyncSession, obj_in: TaskCreate) -> Task:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["deadline"] = datetime.strptime(
            obj_in_data["deadline"], "%Y-%m-%dT%H:%M:%S"
        )
        db_obj = self.model(
            title=obj_in_data["title"],
            description=obj_in_data["description"],
            deadline=obj_in_data["deadline"],
            performers=obj_in_data["performers"],
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_performer(
        self,
        db: AsyncSession,
        *,
        performer_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Task]:
        stmt = (
            select(self.model)
            .filter(self.model.performers == performer_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result


task = CRUDTask(Task)
