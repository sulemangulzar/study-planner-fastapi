from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.models import Subject
from src.subjects.schemas import CreateSubject, UpdateSubject


class SubjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, user_id: UUID):
        result = await self.session.execute(
            select(Subject).where(Subject.user_id == user_id)
        )
        return result.scalars().all()

    async def get_one(self, subject_id: UUID, user_id: UUID):
        result = await self.session.execute(
            select(Subject).where(Subject.id == subject_id, Subject.user_id == user_id)
        )
        subject = result.scalar_one_or_none()

        if subject is None:
            raise HTTPException(status_code=404, detail="Subject not found")

        return subject

    async def create(self, user_id: UUID, data: CreateSubject):
        subject = Subject(name=data.name, user_id=user_id)

        self.session.add(subject)
        await self.session.commit()
        await self.session.refresh(subject)

        return subject

    async def update(self, subject_id: UUID, user_id: UUID, data: UpdateSubject):
        subject = await self.get_one(subject_id, user_id)

        subject.name = data.name

        self.session.add(subject)
        await self.session.commit()
        await self.session.refresh(subject)

        return subject

    async def delete(self, subject_id: UUID, user_id: UUID):
        subject = await self.get_one(subject_id, user_id)

        await self.session.delete(subject)
        await self.session.commit()

        return {"message": "Subject deleted"}
