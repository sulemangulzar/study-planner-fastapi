import jwt
from fastapi import APIRouter, HTTPException, Request

from src.auth.schemas import userCreate, userLogin, userRead
from src.config import settings
from src.dependencies import UserServiceDep

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post("/signup", response_model=userRead, status_code=201)
async def signup(user: userCreate, service: UserServiceDep):
    return await service.create_user(user)


@router.post("/login")
async def login(
    form_data: userLogin,
    service: UserServiceDep,
):
    return await service.login_user(form_data)


@router.get("/is_auth", response_model=userRead)
async def is_auth(request: Request, service: UserServiceDep):
    return await service.is_authenticated(request)


@router.post("/logout")
async def logout():
    pass
