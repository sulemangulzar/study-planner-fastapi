from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class userCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class userLogin(BaseModel):
    username: str
    password: str


class userRead(BaseModel):
    id: UUID | None = None
    name: str
    username: str
    email: EmailStr
    is_active: bool | None = True
    created_at: datetime | None = None
