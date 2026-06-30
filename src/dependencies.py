from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.services import UserService
from src.config import settings
from src.database import get_session
from src.goals.services import GoalService
from src.models.models import User
from src.subjects.services import SubjectService
from src.tasks.services import TaskService

sessionDep = Annotated[AsyncSession, Depends(get_session)]

security = HTTPBearer()


async def get_user_service(session: sessionDep):
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials

    try:
        data = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_id = UUID(data["user"]["id"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token data")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


userAuthDep = Annotated[User, Depends(get_current_user)]


async def get_subject_service(session: sessionDep):
    return SubjectService(session)


SubServiceDep = Annotated[SubjectService, Depends(get_subject_service)]


async def get_task_service(session: sessionDep):
    return TaskService(session)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


async def get_goal_service(session: sessionDep):
    return GoalService(session)


GoalServiceDep = Annotated[GoalService, Depends(get_goal_service)]
