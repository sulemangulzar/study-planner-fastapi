from datetime import datetime

import bcrypt
import jwt
from fastapi import HTTPException, Request
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.schemas import userCreate, userLogin
from src.auth.utils import create_access_token
from src.config import settings
from src.models.models import User


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, creds: userCreate):

        # Check if username already exists
        existing_username = (
            await self.session.execute(
                select(User).where(User.username == creds.username)
            )
        ).scalar_one_or_none()

        if existing_username:
            raise HTTPException(status_code=409, detail="Username already exists")

        # Check if email already exists
        existing_email = (
            await self.session.execute(
                select(User).where(User.email == str(creds.email))
            )
        ).scalar_one_or_none()

        if existing_email:
            raise HTTPException(status_code=409, detail="Email already registered")

        # Create and save the new user
        user = User(
            name=creds.name,
            username=creds.username,
            email=str(creds.email),
            password_hash=get_password_hash(creds.password),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def login_user(self, creds: userLogin):
        result = await self.session.execute(
            select(User).where(User.username == creds.username)
        )
        user = result.scalar_one_or_none()

        if user is None or not verify_password(creds.password, user.password_hash):
            raise HTTPException(
                status_code=401, detail="Username or password is incorrect"
            )

        token = create_access_token(
            data={"user": {"name": user.name, "id": str(user.id)}}
        )

        return {"access_token": token, "token_type": "bearer"}

    async def is_authenticated(self, request: Request):
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = token.split(" ")[-1]

        data = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = data["user"]["id"]

        result = await self.session.execute(select(User).where(User.id == user_id))

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
