from datetime import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field()
    username: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password_hash: str = Field()
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
