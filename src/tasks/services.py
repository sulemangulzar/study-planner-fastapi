from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.models import Subject, Task
from src.tasks.schemas import CreateTask, UpdateTask


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_subject(self, subject_id: UUID | None, user_id: UUID):
        if subject_id is None:
            return

        result = await self.session.execute(
            select(Subject).where(Subject.id == subject_id, Subject.user_id == user_id)
        )
        subject = result.scalar_one_or_none()

        if subject is None:
            raise HTTPException(status_code=404, detail="Subject not found")

    async def get_all(self, user_id: UUID):
        result = await self.session.execute(select(Task).where(Task.user_id == user_id))
        return result.scalars().all()

    async def get_one(self, task_id: UUID, user_id: UUID):
        result = await self.session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return task

    async def create(self, user_id: UUID, data: CreateTask):
        await self.check_subject(data.subject_id, user_id)

        task = Task(
            title=data.title,
            description=data.description,
            due_date=data.due_date,
            subject_id=data.subject_id,
            user_id=user_id,
        )

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def update(self, task_id: UUID, user_id: UUID, data: UpdateTask):
        task = await self.get_one(task_id, user_id)

        if data.subject_id is not None:
            await self.check_subject(data.subject_id, user_id)

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.is_completed is not None:
            task.is_completed = data.is_completed
        if data.due_date is not None:
            task.due_date = data.due_date
        if data.subject_id is not None:
            task.subject_id = data.subject_id

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete(self, task_id: UUID, user_id: UUID):
        task = await self.get_one(task_id, user_id)

        await self.session.delete(task)
        await self.session.commit()

        return {"message": "Task deleted"}
