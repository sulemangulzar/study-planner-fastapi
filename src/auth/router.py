from fastapi import APIRouter

from src.auth.schemas import userCreate, userLogin, userRead
from src.dependencies import UserServiceDep, userAuthDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=userRead, status_code=201)
async def signup(user: userCreate, service: UserServiceDep):
    return await service.create_user(user)


@router.post("/login")
async def login(form_data: userLogin, service: UserServiceDep):
    return await service.login_user(form_data)


@router.get("/is_auth", response_model=userRead)
async def is_auth(user: userAuthDep):
    return user


@router.post("/logout")
async def logout():
    return {"message": "Logout is handled on the frontend by deleting the token"}
