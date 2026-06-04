from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.services import UserService
from src.database import get_session

sessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_service(session: sessionDep):
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
