from uuid import UUID

from fastapi import APIRouter

from src.dependencies import SubServiceDep, userAuthDep
from src.subjects.schemas import CreateSubject, ReadSubject, UpdateSubject

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/", response_model=list[ReadSubject])
async def get_subjects(user: userAuthDep, service: SubServiceDep):
    return await service.get_all(user.id)


@router.post("/", response_model=ReadSubject, status_code=201)
async def create_subject(
    data: CreateSubject, user: userAuthDep, service: SubServiceDep
):
    return await service.create(user.id, data)


@router.get("/{subject_id}", response_model=ReadSubject)
async def get_subject(subject_id: UUID, user: userAuthDep, service: SubServiceDep):
    return await service.get_one(subject_id, user.id)


@router.put("/{subject_id}", response_model=ReadSubject)
async def update_subject(
    subject_id: UUID,
    data: UpdateSubject,
    user: userAuthDep,
    service: SubServiceDep,
):
    return await service.update(subject_id, user.id, data)


@router.delete("/{subject_id}")
async def delete_subject(subject_id: UUID, user: userAuthDep, service: SubServiceDep):
    return await service.delete(subject_id, user.id)
