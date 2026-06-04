from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.auth.schemas import userCreate
from src.auth.utils import create_access_token
from src.models.models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, creds: userCreate):
        user_exists = await self.session.execute(
            select(User).where(col(User.email) == str(creds.email))
        )

        if user_exists.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already registered")

        user = User(
            **creds.model_dump(exclude={"email", "password"}),
            email=str(creds.email),
            password_hash=password_context.hash(creds.password),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def login_user(self, email: str, password: str):
        result = await self.session.execute(
            Select(User).where(col(User.email) == email)
        )
        user = result.scalar_one_or_none()
        if user is None or password_context.verify(password, user.password_hash):
            raise HTTPException(
                status_code=401, detail="Email or password is incorrect"
            )

        token = create_access_token(data={"user": {"name": user.name, "id": user.id}})

        return {"Access Token:": token, "token_type": "bearer"}
