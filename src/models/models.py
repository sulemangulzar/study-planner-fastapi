from datetime import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field()
    username: str = Field(nullable=False, index=True)
    email: EmailStr = Field(nullable=False, index=True)
    password_hash: str = Field()
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Subject(SQLModel, table=True):
    __tablename__ = "subjects"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=100, nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=150, nullable=False)
    description: str | None = Field(default=None)
    is_completed: bool = Field(default=False)
    due_date: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    subject_id: UUID | None = Field(default=None, foreign_key="subjects.id")


class Goal(SQLModel, table=True):
    __tablename__ = "goals"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=150, nullable=False)
    description: str | None = Field(default=None)
    is_completed: bool = Field(default=False)
    target_date: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
