from uuid import UUID

from fastapi import APIRouter

from src.dependencies import TaskServiceDep, userAuthDep
from src.tasks.schemas import CreateTask, ReadTask, UpdateTask

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[ReadTask])
async def get_tasks(user: userAuthDep, service: TaskServiceDep):
    return await service.get_all(user.id)


@router.post("/", response_model=ReadTask, status_code=201)
async def create_task(data: CreateTask, user: userAuthDep, service: TaskServiceDep):
    return await service.create(user.id, data)


@router.get("/{task_id}", response_model=ReadTask)
async def get_task(task_id: UUID, user: userAuthDep, service: TaskServiceDep):
    return await service.get_one(task_id, user.id)


@router.put("/{task_id}", response_model=ReadTask)
async def update_task(
    task_id: UUID,
    data: UpdateTask,
    user: userAuthDep,
    service: TaskServiceDep,
):
    return await service.update(task_id, user.id, data)


@router.delete("/{task_id}")
async def delete_task(task_id: UUID, user: userAuthDep, service: TaskServiceDep):
    return await service.delete(task_id, user.id)
