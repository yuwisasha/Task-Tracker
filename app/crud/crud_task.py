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
        print(obj_in.deadline, type(obj_in.deadline))
        for performer in obj_in.performers:
            stmt = select(User).where(User.id == performer.id)
            performer = await db.execute(stmt)
            db_obj.performers.append(performer.scalar_one_or_none())
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
            .where(self.model.performers.any(User.id == performer_id))
            .offset(skip)
            .limit(limit)
        )
        print(self.model.performers)
        result = await db.execute(stmt)
        return result.scalars().all()


task = CRUDTask(Task)
