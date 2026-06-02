from fastapi import APIRouter

from src.auth.schemas import userCreate, userRead
from src.dependencies import UserServiceDep

router = APIRouter()

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post("/signup", response_model=userRead)
async def signup(user: userCreate, service: UserServiceDep):
    return await service.create_user(user)


@router.post("/login")
async def login():
    pass


@router.post("/logout")
async def logout():
    pass
