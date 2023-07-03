from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def create(self, db: AsyncSession, obj_in: TaskCreate) -> Task:
        db_obj = Task(
            title=obj_in.title,
            description=obj_in.description,
            deadline=obj_in.deadline,
        )
        if obj_in.performers:
            for performer in obj_in.performers:
                stmt = select(User).where(User.id == performer.id)
                performer = await db.execute(stmt)
                db_obj.performers.append(performer.scalar_one())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Task,
        obj_in: TaskUpdate,
    ) -> Task:
        if obj_in.performers:
            for performer in obj_in.performers:
                if performer not in db_obj.performers:
                    stmt = select(User).where(User.id == performer.id)
                    performer = await db.execute(stmt)
                    db_obj.performers.append(performer.scalar_one())
        if obj_in.title:
            db_obj.title = obj_in.title
        if obj_in.description:
            db_obj.description = obj_in.description
        if obj_in.deadline:
            db_obj.deadline = obj_in.deadline
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_performer(
        self,
        db: AsyncSession,
        *,
        performer_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        stmt = (
            select(self.model)
            .where(self.model.performers.any(User.id == performer_id))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()


task = CRUDTask(Task)
