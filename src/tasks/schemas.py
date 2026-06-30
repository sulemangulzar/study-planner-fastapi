from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    subject_id: UUID | None = None


class ReadTask(BaseModel):
    id: UUID
    title: str
    description: str | None
    is_completed: bool
    due_date: datetime | None
    created_at: datetime
    user_id: UUID
    subject_id: UUID | None


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
    due_date: datetime | None = None
    subject_id: UUID | None = None
