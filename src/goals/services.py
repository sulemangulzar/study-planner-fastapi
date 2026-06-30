from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.goals.schemas import CreateGoal, UpdateGoal
from src.models.models import Goal


class GoalService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, user_id: UUID):
        result = await self.session.execute(select(Goal).where(Goal.user_id == user_id))
        return result.scalars().all()

    async def get_one(self, goal_id: UUID, user_id: UUID):
        result = await self.session.execute(
            select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id)
        )
        goal = result.scalar_one_or_none()

        if goal is None:
            raise HTTPException(status_code=404, detail="Goal not found")

        return goal

    async def create(self, user_id: UUID, data: CreateGoal):
        goal = Goal(
            title=data.title,
            description=data.description,
            target_date=data.target_date,
            user_id=user_id,
        )

        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)

        return goal

    async def update(self, goal_id: UUID, user_id: UUID, data: UpdateGoal):
        goal = await self.get_one(goal_id, user_id)

        if data.title is not None:
            goal.title = data.title
        if data.description is not None:
            goal.description = data.description
        if data.is_completed is not None:
            goal.is_completed = data.is_completed
        if data.target_date is not None:
            goal.target_date = data.target_date

        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)

        return goal

    async def delete(self, goal_id: UUID, user_id: UUID):
        goal = await self.get_one(goal_id, user_id)

        await self.session.delete(goal)
        await self.session.commit()

        return {"message": "Goal deleted"}
