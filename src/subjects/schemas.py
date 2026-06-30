from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateSubject(BaseModel):
    name: str


class ReadSubject(BaseModel):
    id: UUID
    name: str

    created_at: datetime
    user_id: UUID


class UpdateSubject(BaseModel):
    name: str
