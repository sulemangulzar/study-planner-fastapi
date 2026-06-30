from uuid import UUID

from fastapi import APIRouter

from src.dependencies import GoalServiceDep, userAuthDep
from src.goals.schemas import CreateGoal, ReadGoal, UpdateGoal

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/", response_model=list[ReadGoal])
async def get_goals(user: userAuthDep, service: GoalServiceDep):
    return await service.get_all(user.id)


@router.post("/", response_model=ReadGoal, status_code=201)
async def create_goal(data: CreateGoal, user: userAuthDep, service: GoalServiceDep):
    return await service.create(user.id, data)


@router.get("/{goal_id}", response_model=ReadGoal)
async def get_goal(goal_id: UUID, user: userAuthDep, service: GoalServiceDep):
    return await service.get_one(goal_id, user.id)


@router.put("/{goal_id}", response_model=ReadGoal)
async def update_goal(
    goal_id: UUID,
    data: UpdateGoal,
    user: userAuthDep,
    service: GoalServiceDep,
):
    return await service.update(goal_id, user.id, data)


@router.delete("/{goal_id}")
async def delete_goal(goal_id: UUID, user: userAuthDep, service: GoalServiceDep):
    return await service.delete(goal_id, user.id)
