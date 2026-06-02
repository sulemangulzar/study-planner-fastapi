from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.models.models import User
from src.users.schemas import UserCreate

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, creds: UserCreate):
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
