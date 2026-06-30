from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateGoal(BaseModel):
    title: str
    description: str | None = None
    target_date: datetime | None = None


class ReadGoal(BaseModel):
    id: UUID
    title: str
    description: str | None
    is_completed: bool
    target_date: datetime | None
    created_at: datetime
    user_id: UUID


class UpdateGoal(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
    target_date: datetime | None = None
