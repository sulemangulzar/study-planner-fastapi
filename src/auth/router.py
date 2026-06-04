from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.ifc import log

from src.auth.schemas import userCreate, userRead
from src.dependencies import UserServiceDep

router = APIRouter()

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post("/signup", response_model=userRead)
async def signup(user: userCreate, service: UserServiceDep):
    return await service.create_user(user)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
):
    return await service.login_user(form_data.username, form_data.password)


@router.post("/logout")
async def logout():
    pass
