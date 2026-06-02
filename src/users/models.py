from datetime import datetime, timezone
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: UUID = Field(sa_column=Column(postgresql.UUID, default=None, primary_key=True))
    name: str = Field(max_length=100)
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    hashed_password: str

    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
